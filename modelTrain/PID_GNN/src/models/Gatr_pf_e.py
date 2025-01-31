from os import path
import sys

# sys.path.append(
#     path.abspath("/afs/cern.ch/work/m/mgarciam/private/geometric-algebra-transformer/")
# )
# sys.path.append(path.abspath("/mnt/proj3/dd-23-91/cern/geometric-algebra-transformer/"))
from time import time
from gatr import GATr, SelfAttentionConfig, MLPConfig
from gatr.interface import embed_point, extract_scalar, extract_point, embed_scalar
from torch_scatter import scatter_add, scatter_mean
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
        number_of_classes = 2
        # self.clustering = nn.Linear(16, number_of_classes, bias=False)
        # self.loss_crit = nn.CrossEntropyLoss()
        self.loss_crit = nn.BCELoss()
        self.m = nn.Sigmoid()
        self.readout = "sum"
        self.MLP_layer = MLPReadout(17 + 3, number_of_classes)

    def forward(self, g, step_count, eval="", return_train=False):
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
        # if self.trainer.is_global_zero and step_count % 500 == 0:
        #     g.ndata["original_coords"] = g.ndata["pos_hits_xyz"]
        #     PlotCoordinates(
        #         g,
        #         path="input_coords",
        #         outdir=self.args.model_prefix,
        #         # features_type="ones",
        #         predict=self.args.predict,
        #         epoch=str(self.current_epoch) + eval,
        #         step_count=step_count,
        #     )
        inputs_scalar = g.ndata["hit_type"].view(-1, 1)
        inputs = self.ScaledGooeyBatchNorm2_1(inputs)
        # inputs = inputs.unsqueeze(0)
        embedded_inputs = embed_point(inputs)  # + embed_scalar(inputs_scalar)
        embedded_inputs = embedded_inputs.unsqueeze(
            -2
        )  # (batch_size*num_points, 1, 16)
        mask = self.build_attention_mask(g)
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

        if self.readout == "sum":
            hg = dgl.sum_nodes(g, "h")
        elif self.readout == "max":
            hg = dgl.max_nodes(g, "h")
        elif self.readout == "mean":
            hg = dgl.mean_nodes(g, "h")
        else:
            hg = dgl.mean_nodes(g, "h")  # default readout is mean nodes

        ## head 2
        g.ndata["hit_type1"] = 1.0 * (g.ndata["hit_type"] == 1)
        g.ndata["hit_type2"] = 1.0 * (g.ndata["hit_type"] == 2)
        g.ndata["hit_type3"] = 1.0 * (g.ndata["hit_type"] == 3)
        feature_high_level = torch.cat(
            (
                dgl.sum_nodes(g, "hit_type1").view(-1, 1),
                dgl.mean_nodes(g, "hit_type2").view(-1, 1),
                dgl.mean_nodes(g, "hit_type3").view(-1, 1),
            ),
            dim=1,
        )
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
        batch_numbers = obtain_batch_numbers(g)
        return BlockDiagonalMask.from_seqlens(
            torch.bincount(batch_numbers.long()).tolist()
        )

    def training_step(self, batch, batch_idx):
        y = batch[1]
        batch_g = batch[0]
        initial_time = time()
        if self.trainer.is_global_zero:
            model_output = self(batch_g, batch_idx)
        else:
            model_output = self(batch_g, 1)
        loss_time_start = time()

        # Dummy loss to avoid errors
        labels_true = dgl.readout_nodes(batch_g, "label_true", op="max")

        labels_true[labels_true == 4] = 1
        loss = self.loss_crit(
            self.m(model_output),
            1.0 * F.one_hot(labels_true.view(-1).long(), num_classes=2),
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
        self.validation_step_outputs = []
        y = batch[1]
        batch_g = batch[0]
        shap_vals, ec_x = None, None

        model_output = self(batch_g, 1)
        labels_true = dgl.readout_nodes(batch_g, "label_true", op="max")
        labels_true[labels_true == 4] = 1
        # create_and_store_graph_output(
        #     labels_true,
        #     batch_g,
        #     model_output,
        #     y,
        #     batch_idx,
        #     path_save=self.args.model_prefix,
        # )
        loss = self.loss_crit(
            self.m(model_output),
            1.0 * F.one_hot(labels_true.view(-1).long(), num_classes=2),
        )
        # m = nn.Softmax(dim=1)
        model_output1 = self.m(model_output)
        if self.args.predict:
            d = {
                "pion0": model_output1.detach().cpu()[:, 0].view(-1),
                "pion": model_output1.detach().cpu()[:, 1].view(-1),
                "e": model_output1.detach().cpu()[:, 2].view(-1),
                "muon": model_output1.detach().cpu()[:, 3].view(-1),
                "rho": model_output1.detach().cpu()[:, 4].view(-1),
                "labels_true": labels_true.detach().cpu().view(-1),
                "energy": y.E.detach().cpu().view(-1),
            }
        # if self.args.predict:
        #     d = {
        #         "pion": model_output1.detach().cpu()[:, 0].view(-1),
        #         "rho": model_output1.detach().cpu()[:, 1].view(-1),
        #         "labels_true": labels_true.detach().cpu().view(-1),
        #         "energy": y.E.detach().cpu().view(-1),
        #     }
            df = pd.DataFrame(data=d)
            self.eval_df.append(df)

        if self.trainer.is_global_zero:
            wandb.log({"loss_val": loss.item()})
            acc = torch.mean(
                1.0 * (model_output.argmax(axis=1) == labels_true.view(-1))
            )
            wandb.log({"accuracy val ": acc.item()})

        if self.trainer.is_global_zero:
            wandb.log(
                {
                    "conf_mat": wandb.plot.confusion_matrix(
                        probs=None,
                        y_true=labels_true.view(-1).detach().cpu().numpy(),
                        preds=model_output.argmax(axis=1)
                        .view(-1)
                        .detach()
                        .cpu()
                        .numpy(),
                        # class_names=["pi0", "pi", "e+", "mu", "rho"],
                        class_names=["pi", "rho"],
                    )
                }
            )

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
            df_batch1.to_pickle(self.args.model_prefix + "/model_output_eval.pt")

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
        print("Optimizer params:", filter(lambda p: p.requires_grad, self.parameters()))
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


def obtain_batch_numbers(g):
    graphs_eval = dgl.unbatch(g)
    number_graphs = len(graphs_eval)
    batch_numbers = []
    for index in range(0, number_graphs):
        gj = graphs_eval[index]
        num_nodes = gj.number_of_nodes()
        batch_numbers.append(index * torch.ones(num_nodes))
        num_nodes = gj.number_of_nodes()

    batch = torch.cat(batch_numbers, dim=0)
    return batch