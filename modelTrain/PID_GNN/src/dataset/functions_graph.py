import numpy as np
import torch
import dgl
from torch_scatter import scatter_add, scatter_sum
from sklearn.preprocessing import StandardScaler
from torch_scatter import scatter_sum
from src.dataset.functions_data import (
    get_ratios,
    find_mask_no_energy,
    find_cluster_id,
    get_particle_features,
    get_hit_features,
    calculate_distance_to_boundary,
    concatenate_Particles_GT,
)


def create_inputs_from_table(
    output, hits_only, prediction=False, hit_chis=False, tau_sample=False
):
    """Used by graph creation to get nodes and edge features

    Args:
        output (_type_): input from the root reading
        hits_only (_type_): reading only hits or also tracks
        prediction (bool, optional): if running in eval mode. Defaults to False.

    Returns:
        _type_: all information to construct a graph
    """
    number_hits = np.int32(np.sum(output["pf_mask"][0]))
    number_part = np.int32(np.sum(output["pf_mask"][1]))

    (
        pos_xyz_hits,
        pos_pxpypz,
        p_hits,
        e_hits,
        hit_particle_link,
        pandora_cluster,
        pandora_cluster_energy,
        pfo_energy,
        unique_list_particles,
        cluster_id,
        hit_type_feature,
        pandora_pfo_link,
        daughters,
        hit_link_modified,
        connection_list,
        chi_squared_tracks,
        labels_true,
        tau_label,
    ) = get_hit_features(
        output,
        number_hits,
        prediction,
        number_part,
        hit_chis=hit_chis,
        tau_sample=tau_sample,
    )
    # print("unique_list_particles", unique_list_particles)
    # features particles
    y_data_graph = get_particle_features(
        unique_list_particles,
        output,
        prediction,
        connection_list,
        tau_sample=tau_sample,
    )

    # assert len(y_data_graph) == len(unique_list_particles)

    result = [
        y_data_graph,  # y_data_graph[~mask_particles],
        p_hits,
        e_hits,
        daughters,
        cluster_id,
        hit_particle_link,
        pos_xyz_hits,
        pos_pxpypz,
        pandora_cluster,
        pandora_cluster_energy,
        pfo_energy,
        pandora_pfo_link,
        hit_type_feature,
        hit_link_modified,
        labels_true,
        tau_label,
    ]
    if hit_chis:
        result.append(
            chi_squared_tracks,
        )
    else:
        result.append(None)
    hit_type = hit_type_feature
    # if hits only remove tracks, otherwise leave tracks

    # if we want the tracks keep only 1 track hit per charged particle.
    hit_mask = hit_type == 0
    hit_mask = ~hit_mask
    for i in range(1, len(result)):
        if result[i] is not None:
            result[i] = result[i][hit_mask]
    hit_type_one_hot = torch.nn.functional.one_hot(
        hit_type_feature[hit_mask] - 1, num_classes=3
    )

    result.append(hit_type_one_hot)
    result.append(connection_list)
    return result


def create_graph(
    output,
    config=None,
    n_noise=0,
):
    hits_only = config.graph_config.get(
        "only_hits", False
    )  # Whether to only include hits in the graph
    # standardize_coords = config.graph_config.get("standardize_coords", False)
    extended_coords = config.graph_config.get("extended_coords", False)
    prediction = config.graph_config.get("prediction", False)
    hit_chis = config.graph_config.get("hit_chis_track", False)
    tau_sample = config.graph_config.get("tau_sample", False)
    (
        y_data_graph,
        p_hits,
        e_hits,
        daughters,
        cluster_id,
        hit_particle_link,
        pos_xyz_hits,
        pos_pxpypz,
        pandora_cluster,
        pandora_cluster_energy,
        pandora_pfo_energy,
        pandora_pfo_link,
        hit_type,
        hit_link_modified,
        labels_true,
        tau_label,
        chi_squared_tracks,
        hit_type_one_hot,
        connections_list,
    ) = create_inputs_from_table(
        output,
        hits_only=hits_only,
        prediction=prediction,
        hit_chis=hit_chis,
        tau_sample=tau_sample,
    )
    # print("pandora_pfo_link", pandora_pfo_link[hit_type == 1])
    graph_coordinates = pos_xyz_hits  # / 3330  # divide by detector size
    if pos_xyz_hits.shape[0] > 0:
        graph_empty = False
        g = dgl.graph(([], []))
        g.add_nodes(graph_coordinates.shape[0])

        hit_features_graph = torch.cat(
            (graph_coordinates, hit_type_one_hot, e_hits, p_hits), dim=1
        )

        if tau_sample:
            sorted_index = torch.sort(tau_label.long().view(1, -1))[1].view(-1)
            g.ndata["h"] = hit_features_graph[sorted_index]
            g.ndata["pos_hits_xyz"] = pos_xyz_hits[sorted_index]
            g.ndata["pos_pxpypz"] = pos_pxpypz[sorted_index]
            g.ndata["label_true"] = 1.0 * labels_true[sorted_index].view(-1, 1)
            g.ndata["tau_label"] = 1.0 * tau_label[sorted_index].view(-1, 1)
            g.ndata["hit_type"] = hit_type[sorted_index]
            g.ndata["daughters"] = daughters[sorted_index]
            g.ndata["e_hits"] = e_hits[sorted_index]
            g.ndata["p_hits"] = p_hits[sorted_index]  #

            g.ndata["particle_number"] = cluster_id[sorted_index]
            g.ndata["hit_link_modified"] = hit_link_modified[sorted_index]
            g.ndata["particle_number_nomap"] = hit_particle_link[sorted_index]
            if prediction:
                g.ndata["pandora_cluster"] = pandora_cluster[sorted_index]
                g.ndata["pandora_pfo"] = pandora_pfo_link[sorted_index]
                g.ndata["pandora_cluster_energy"] = pandora_cluster_energy[sorted_index]
                g.ndata["pandora_pfo_energy"] = pandora_pfo_energy[sorted_index]

        else:
            g.ndata["h"] = hit_features_graph
            g.ndata["pos_hits_xyz"] = pos_xyz_hits
            g.ndata["pos_pxpypz"] = pos_pxpypz
            g.ndata["label_true"] = 1.0 * labels_true.view(-1, 1)
            if tau_sample:
                g.ndata["tau_label"] = 1.0 * tau_label.view(-1, 1)

            g.ndata["hit_type"] = hit_type  
            g.ndata["daughters"] = daughters
            g.ndata["e_hits"] = e_hits
            g.ndata["p_hits"] = p_hits  #
            if hit_chis:
                g.ndata["chi_squared_tracks"] = chi_squared_tracks
            g.ndata["particle_number"] = cluster_id
            g.ndata["hit_link_modified"] = hit_link_modified
            g.ndata["particle_number_nomap"] = hit_particle_link
            g.ndata["label_true"] = labels_true
            if prediction:
                g.ndata["pandora_cluster"] = pandora_cluster
                g.ndata["pandora_pfo"] = pandora_pfo_link
                g.ndata["pandora_cluster_energy"] = pandora_cluster_energy
                g.ndata["pandora_pfo_energy"] = pandora_pfo_energy

        # remove particles from ISR
        if tau_sample:
            g = dgl.remove_nodes(g, torch.where(g.ndata["tau_label"] == -1)[0])
    #
    # check decay types:
    if tau_sample and not graph_empty:
        index_labels = torch.Tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 10, 10]).to(
            labels_true.device
        )
        labels_true = g.ndata["label_true"]
        g.ndata["label_true"] = index_labels[labels_true.long()]
    if tau_sample:
        decay_types = torch.unique(g.ndata["label_true"])
        # print("decay types", decay_types)
        if torch.sum(decay_types == 10) == 2:
            graph_empty = True
        # elif (torch.sum(decay_types == 10) == 1) and (torch.sum(decay_types == 4) == 1):
        #     graph_empty = True
        elif torch.sum(decay_types == 10) == 1:
            g = dgl.remove_nodes(g, torch.where(g.ndata["label_true"] == 10)[0])
        # elif torch.sum(decay_types == 4) == 1:
        #     g = dgl.remove_nodes(g, torch.where(g.ndata["label_true"] == 4)[0])
        # elif torch.sum(decay_types == 4) == 2:
        #     graph_empty = True
    # g = dgl.remove_nodes(g, torch.where(g.ndata["tau_label"] == 11)[0])
    # print('found one 10 decay')
    # else the two tau decays are part of the decays we know and love

    if len(g.ndata["label_true"]) < 10:
        graph_empty = True
    # # print("graph_empty", graph_empty)

    return [g, y_data_graph], graph_empty


def graph_batch_func(list_graphs):
    """collator function for graph dataloader

    Args:
        list_graphs (list): list of graphs from the iterable dataset

    Returns:
        batch dgl: dgl batch of graphs
    """
    list_graphs_g = [el[0] for el in list_graphs]
    # list_y = add_batch_number(list_graphs)
    # ys = torch.cat(list_y, dim=0)
    # ys = torch.reshape(ys, [-1, list_y[0].shape[1]])
    ys = concatenate_Particles_GT(list_graphs)
    bg = dgl.batch(list_graphs_g)
    # reindex particle number
    return bg, ys