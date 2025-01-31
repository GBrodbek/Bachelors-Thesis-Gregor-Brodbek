from os import path
import sys

# sys.path.append(
#     path.abspath("/afs/cern.ch/work/m/mgarciam/private/geometric-algebra-transformer/")
# )
# sys.path.append(path.abspath("/mnt/proj3/dd-23-91/cern/geometric-algebra-transformer/"))
from time import time
from gatr import GATr, SelfAttentionConfig, MLPConfig
from gatr.interface import embed_point, extract_scalar, extract_point, embed_scalar
from torch_scatter import scatter_add, scatter_mean, scatter_max
import torch
import torch.nn as nn
from src.utils.save_features import save_features
#from src.logger.plotting_tools import PlotCoordinates
import numpy as np
from typing import Tuple, Union, List
import dgl
#from src.logger.plotting_tools import PlotCoordinates
from src.models.mlp_readout_layer import MLPReadout

import pytorch_lightning as L
from torch.optim.lr_scheduler import ReduceLROnPlateau, StepLR
from src.layers.inference_oc import create_and_store_graph_output
from xformers.ops.fmha import BlockDiagonalMask
import os
import wandb

import torch.nn.functional as F
import pandas as pd

from sklearn.utils.class_weight import compute_class_weight


class ExampleWrapper(L.LightningModule):
    """Example wrapper around a GATr model.

    Expects input data that consists of a point cloud: one 3D point for each item in the data.
    Returns outputs that consists of one scalar number for the whole dataset.

    Parameters
    ----------
    blocks : int
        Number of transformer blocks
    hidden_mv_channels : int
        Number of hidden multivector channels
    hidden_s_channels : int
        Number of hidden scalar channels
    """

    def __init__(
        self,
        args,
        dev,
        input_dim: int = 5,
        output_dim: int = 4,
        n_postgn_dense_blocks: int = 3,
        n_gravnet_blocks: int = 4,
        clust_space_norm: str = "twonorm",
        k_gravnet: int = 7,
        activation: str = "elu",
        weird_batchnom=False,
        blocks=10,
        hidden_mv_channels=16,
        hidden_s_channels=64,
    ):
        super().__init__()
        self.strict_loading = False
        self.input_dim = 3
        self.output_dim = 4
        self.loss_final = 0
        self.number_b = 0
        self.df_showers = []
        self.df_showers_pandora = []
        self.df_showes_db = []
        self.validation_step_outputs = []
        self.args = args
        self.gatr = GATr(
            in_mv_channels=1,
            out_mv_channels=1,
            hidden_mv_channels=hidden_mv_channels,
            in_s_channels=3,
            out_s_channels=1,
            hidden_s_channels=hidden_s_channels,
            num_blocks=blocks,
            attention=SelfAttentionConfig(),  # Use default parameters for attention
            mlp=MLPConfig(),  # Use default parameters for MLP
        )
        self.ScaledGooeyBatchNorm2_1 = nn.BatchNorm1d(self.input_dim, momentum=0.1)
        #number_of_classes = 4
        # self.clustering = nn.Linear(16, number_of_classes, bias=False)
        self.loss_crit = nn.BCELoss()
        # self.loss_crit = nn.BCELoss()

        self.readout = "sum"
        self.MLP_layer = MLPReadout(17 + 3, 9)
        self.m = nn.Sigmoid()

    def obtain_loss_weighted(self, labels_true):
        # class_weights = compute_class_weight(
        #     "balanced",
        #     classes=torch.unique(labels_true).detach().cpu().numpy(),
        #     y=labels_true.detach().cpu().numpy(),
        # )
        w_e = 1 / 0.17
        w_mu = 1 / 0.18
        w_pi_pi0 = 1 / 0.25
        w_pi = 1 / 0.11
        w_pi_2pi0 = 1 / 0.09
        w_3pi = 1 / 0.09
        w_3pi_pi0 = 1 / 0.05
        w_background = 1 / 0.4
        w_bhabha = 1 / 0.2

        # w_rho = 1 / 0.25
        # w_pi = 1 / 0.10

        class_weights = torch.tensor([w_e, w_mu, w_pi_pi0, w_pi, w_pi_2pi0, w_3pi, w_3pi_pi0, w_background, w_bhabha]).to(labels_true.device)
        # unique_class_labels = torch.unique(labels_true).long()
        unique_class_labels = torch.arange(9).long().to(labels_true.device)
        # weights_all_classes = torch.zeros(4).to(unique_class_labels.device)
        # weights_all_classes[unique_class_labels] = torch.Tensor(class_weights).to(
        #     unique_class_labels.device
        # )

        self.loss_crit = nn.BCELoss(weight=class_weights[unique_class_labels])

    def forward(self, g, step_count, mask, labels, eval="", return_train=False):
        """Forward pass.

        Parameters
        ----------
        inputs : torch.Tensor with shape (*batch_dimensions, num_points, 3)
            Point cloud input data

        Returns
        -------
        outputs : torch.Tensor with shape (*batch_dimensions, 1)
            Model prediction: a single scalar for the whole point cloud.
        """

        inputs = g.ndata["pos_hits_xyz"]

        inputs_scalar = g.ndata["hit_type"].view(-1, 1)
        inputs = self.ScaledGooeyBatchNorm2_1(inputs)

        embedded_inputs = embed_point(inputs)  # + embed_scalar(inputs_scalar)
        embedded_inputs = embedded_inputs.unsqueeze(
            -2
        )  # (batch_size*num_points, 1, 16)

        scalars = torch.zeros((inputs.shape[0], 1))
        scalars = torch.cat(
            (g.ndata["h"][:, -2:], inputs_scalar), dim=1
        )  # this corresponds to e,p
        # Pass data through GATr
        embedded_outputs, scalar_outputs = self.gatr(
            embedded_inputs, scalars=scalars, attention_mask=mask
        )  # (..., num_points, 1, 16)
        # wandb.log({"time_gatr_pass": forward_time_end - forward_time_start})
        # points = extract_point(embedded_outputs[:, 0, :])

        # # Extract scalar and aggregate outputs from point cloud
        # nodewise_outputs = extract_scalar(embedded_outputs)  # (..., num_points, 1, 1)
        # x_point = points
        # x_scalar = torch.cat(
        #     (nodewise_outputs.view(-1, 1), scalar_outputs.view(-1, 1)), dim=1
        # )
        # output = torch.cat(
        #     (embedded_outputs[:, 0, :], scalar_outputs.view(-1, 1)), dim=1
        # )
        g.ndata["h"] = torch.cat(
            (embedded_outputs[:, 0, :], scalar_outputs.view(-1, 1)), dim=1
        )
        hg = graph_sum_output(labels, g.ndata["h"])
        ## head 2
        g.ndata["hit_type1"] = 1.0 * (g.ndata["hit_type"] == 1)
        g.ndata["hit_type2"] = 1.0 * (g.ndata["hit_type"] == 2)
        g.ndata["hit_type3"] = 1.0 * (g.ndata["hit_type"] == 3)

        feature_high_level = torch.cat(
            (
                scatter_add(g.ndata["hit_type1"].view(-1), labels.long().view(-1)).view(
                    -1, 1
                ),
                scatter_add(g.ndata["hit_type2"].view(-1), labels.long().view(-1)).view(
                    -1, 1
                ),
                scatter_add(g.ndata["hit_type3"].view(-1), labels.long().view(-1)).view(
                    -1, 1
                ),
            ),
            dim=1,
        )

        # all_features = hg.view(
        #     -1, 17
        # )
        all_features = torch.cat((feature_high_level, hg.view(-1, 17)), dim=1)

        all_features = self.MLP_layer(all_features)
        return all_features

    def build_attention_mask(self, g):
        """Construct attention mask from pytorch geometric batch.

        Parameters
        ----------
        inputs : torch_geometric.data.Batch
            Data batch.

        Returns
        -------
        attention_mask : xformers.ops.fmha.BlockDiagonalMask
            Block-diagonal attention mask: within each sample, each token can attend to each other
            token.
        """
        batch_numbers = obtain_batch_numbers_tau(g)

        return (
            BlockDiagonalMask.from_seqlens(
                torch.bincount(batch_numbers.long()).tolist()
            ),
            batch_numbers,
        )

    def training_step(self, batch, batch_idx):
        y = batch[1]
        batch_g = batch[0]
        initial_time = time()
        mask, labels = self.build_attention_mask(batch_g)

        if self.trainer.is_global_zero:
            model_output = self(batch_g, batch_idx, mask, labels)
        else:
            model_output = self(batch_g, 1, mask, labels)
        loss_time_start = time()

        # rho is 2
        # pi is 3

        labels_true = scatter_max(batch_g.ndata["label_true"].view(-1), labels.long())[
            0
        ]
        self.obtain_loss_weighted(labels_true)
        loss = self.loss_crit(
            torch.sigmoid(model_output),
            1.0 * F.one_hot(labels_true.view(-1).long(), num_classes=9),
        )
        loss_time_end = time()
        if self.trainer.is_global_zero:
            wandb.log(
                {"loss_comp_time_inside_training": loss_time_end - loss_time_start}
            )

        misc_time_start = time()
        if self.trainer.is_global_zero:
            wandb.log({"loss": loss.item()})
            acc = torch.mean(
                1.0 * (model_output.argmax(axis=1) == labels_true.view(-1))
            )
            wandb.log({"accuracy": acc.item()})
        self.loss_final = loss.item() + self.loss_final
        self.number_b = self.number_b + 1
        del model_output

        final_time = time()
        if self.trainer.is_global_zero:
            wandb.log({"misc_time_inside_training": final_time - misc_time_start})
            wandb.log({"training_step_time": final_time - initial_time})
        return loss

    def validation_step(self, batch, batch_idx):
        cluster_features_path = os.path.join(self.args.model_prefix, "cluster_features")
        show_df_eval_path = os.path.join(
            self.args.model_prefix, "showers_df_evaluation"
        )
        if not os.path.exists(show_df_eval_path):
            os.makedirs(show_df_eval_path)
        if not os.path.exists(cluster_features_path):
            os.makedirs(cluster_features_path)
        # self.validation_step_outputs = []
        y = batch[1]
        batch_g = batch[0]
        shap_vals, ec_x = None, None
        mask, labels = self.build_attention_mask(batch_g)
        model_output = self(batch_g, 1, mask, labels)
        labels_true = scatter_max(batch_g.ndata["label_true"].view(-1), labels.long())[
            0
        ]
        energies = scatter_max(batch_g.ndata["e_hits"].view(-1), labels.long())[0]
        # create_and_store_graph_output(
        #     labels_true,
        #     batch_g,
        #     model_output,
        #     y,
        #     batch_idx,
        #     path_save=self.args.model_prefix,
        # )
        self.obtain_loss_weighted(labels_true)
        loss = self.loss_crit(
            torch.sigmoid(model_output),
            1.0 * F.one_hot(labels_true.view(-1).long(), num_classes=9),
        )

        model_output1 = model_output
        if self.args.predict:
            d = {
                "e": model_output1.detach().cpu()[:, 0].view(-1),          # is it correct sequence? is not 0 e, 1 mu, ...
                "mu": model_output1.detach().cpu()[:, 1].view(-1),
                "pi_pi0": model_output1.detach().cpu()[:, 2].view(-1),
                "pi": model_output1.detach().cpu()[:, 3].view(-1),
                "pi_2pi0": model_output1.detach().cpu()[:, 4].view(-1),
                "3pi": model_output1.detach().cpu()[:, 5].view(-1),
                "3pi_pi0": model_output1.detach().cpu()[:, 6].view(-1),
                "qq background": model_output1.detach().cpu()[:, 7].view(-1),
                "Bhabha": model_output1.detach().cpu()[:, 8].view(-1),
                "labels_true": labels_true.detach().cpu().view(-1),
                "energy": energies.detach().cpu().view(-1),                 #y.E.detach().cpu().view(-1)
            }
            #d = {
            #    "rho": model_output1.detach().cpu()[:, 0].view(-1),
            #    "pi": model_output1.detach().cpu()[:, 1].view(-1),
            #    "labels_true": labels_true.detach().cpu().view(-1),
            #    "energy": energies.detach().cpu().view(-1),
            #}
            df = pd.DataFrame(data=d)
            self.eval_df.append(df)


        # accumulate predictions and true labels from all batches
        preds_batch = model_output.argmax(axis=1).view(-1).detach().cpu().numpy()
        labels_true_batch = labels_true.view(-1).detach().cpu().numpy()
        probs_batch = model_output.detach().cpu().numpy()

        self.validation_step_outputs.append((preds_batch, labels_true_batch, probs_batch))

        # if self.trainer.is_global_zero:
        # print(model_output)
        # print(labels_true)
        wandb.log({"loss_val": loss.item()})
        acc = torch.mean(1.0 * (model_output.argmax(axis=1) == labels_true.view(-1)))
        # print(acc)
        wandb.log({"accuracy val ": acc.item()})

        # if self.trainer.is_global_zero:
        # wandb.log(
        #     {
        #         "conf_mat": wandb.plot.confusion_matrix(
        #             probs=None,
        #             y_true=labels_true.view(-1).detach().cpu().numpy(),
        #             preds=model_output.argmax(axis=1).view(-1).detach().cpu().numpy(),
        #             class_names=["e", "mu", "pi", "pi pi0", "rpi 2pi0", "3pi", "3pi pi0", "background"],
        #             #class_names=["rho", "pi"],
        #         )
        #     }
        # )

        del loss
        del model_output

    def on_train_epoch_end(self):

        self.log("train_loss_epoch", self.loss_final / self.number_b)

    def on_train_epoch_start(self):
        # if self.trainer.is_global_zero and self.current_epoch == 0:
        #     self.stat_dict = {}
        self.make_mom_zero()

    def on_validation_epoch_start(self):
        self.make_mom_zero()
        self.eval_df = []

    def on_validation_epoch_end(self):
        if self.args.predict:
            df_batch1 = pd.concat(self.eval_df)
            df_batch1.to_pickle(self.args.model_prefix + f"/model_output_eval_logits_{self.args.wandb_displayname}.pt")

        all_preds = []
        all_labels = []
        all_probs = []

        # Gather predictions and true labels from all batches
        for preds, labels_true, probs in self.validation_step_outputs:
            all_preds.extend(preds)
            all_labels.extend(labels_true)
            all_probs.extend(probs)

        # Compute confusion matrix
        wandb.log(
            {
                "conf_mat": wandb.plot.confusion_matrix(
                    probs=None,
                    y_true=all_labels,
                    preds=all_preds,
                    class_names=["0: e", "1: mu", "2: pi pi0", "3: pi", "4: pi 2pi0", "5: 3pi", "6: 3pi pi0", "7: qq background", "8: Bhabha"],
                )
            }
        )

        
        wandb.log({"roc" : wandb.plot.roc_curve(all_labels, all_probs, labels=None, classes_to_plot=None)})

        # Clear validation_step_outputs for the next epoch
        self.validation_step_outputs = []    

    # def on_after_backward(self):
    #     for name, p in self.named_parameters():
    #         if p.grad is None:
    #             print(name)

    def make_mom_zero(self):
        if self.current_epoch > 1 or self.args.predict:
            print("making momentum 0")
            self.ScaledGooeyBatchNorm2_1.momentum = 0

    # def on_validation_epoch_end(self):

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, self.parameters()), lr=1e-3
        )
        # print("Optimizer params:", filter(lambda p: p.requires_grad, self.parameters()))
        # print("Optimizer params:", list(filter(lambda p: p.requires_grad, self.parameters())))

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": ReduceLROnPlateau(optimizer, patience=3),
                "interval": "epoch",
                "monitor": "train_loss_epoch",
                "frequency": 1
                # If "monitor" references validation metrics, then "frequency" should be set to a
                # multiple of "trainer.check_val_every_n_epoch".
            },
        }


def obtain_batch_numbers_tau(g):
    graphs_eval = dgl.unbatch(g)
    number_graphs = len(graphs_eval)
    batch_numbers = []
    counter_index = 0
    for index in range(0, number_graphs):
        gj = graphs_eval[index]
        number_of_graphs = torch.unique(gj.ndata["tau_label"])
        for el in range(0, len(number_of_graphs)):
            g1_number_of_nodes = torch.sum(
                gj.ndata["tau_label"] == number_of_graphs[el]
            )
            batch_numbers.append(
                counter_index
                * torch.ones(g1_number_of_nodes).to(gj.ndata["tau_label"].device)
            )
            counter_index = counter_index + 1

    batch = torch.cat(batch_numbers, dim=0)
    return batch


def graph_sum_output(labels, h):
    tensor = h
    num_fea = h.shape[-1]
    unique_indices, inverse_indices = torch.unique(labels, return_inverse=True)
    unique_indices = unique_indices.to(h.device)
    inverse_indices = inverse_indices.to(h.device)
    output = torch.zeros((len(unique_indices), num_fea)).to(h.device)
    output.scatter_add_(0, inverse_indices.unsqueeze(1).expand(-1, num_fea), tensor)
    return output