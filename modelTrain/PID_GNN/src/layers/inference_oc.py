import dgl
import torch
import os
from sklearn.cluster import DBSCAN, HDBSCAN
from torch_scatter import scatter_max, scatter_add, scatter_mean
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
import pandas as pd
import wandb


def create_and_store_graph_output(
    labels_true, batch_g, model_output, y, step, path_save
):
    list_graphs = dgl.unbatch(batch_g)
    batch_id = y.batch_number.view(-1)
    for i, g_i in enumerate(list_graphs):
        mask = batch_id == i
        y1 = y.copy()
        y1.mask(mask)
        # print(y1)
        label_i = labels_true[i]
        pred_i = model_output[i]
        print(label_i != torch.argmax(pred_i.view(-1)))
        if label_i != torch.argmax(pred_i.view(-1)):
            str_label = int(label_i.detach().cpu().numpy())
            str_pred = int(torch.argmax(pred_i.view(-1)).detach().cpu().numpy())
            path = (
                path_save
                + "/graphs_all_comparing_root_t1/"
                + str(str_label)
                + "_"
                + str(str_pred)
                + "/"
            )
            if not os.path.exists(path):
                os.makedirs(path)
            dic = {}
            dic["graph"] = g_i
            dic["model_output"] = model_output[i]
            dic["y1"] = y1.pid
            dic["y1_E"] = y1.E
            torch.save(
                dic,
                path + "_" + str(step) + "_" + str(i) + ".pt",
            )
