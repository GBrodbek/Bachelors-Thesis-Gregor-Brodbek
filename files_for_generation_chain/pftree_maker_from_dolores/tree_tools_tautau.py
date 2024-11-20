import sys
import math
import ROOT
from array import array
from ROOT import TFile, TTree
import numpy as np
from podio import root_io
import edm4hep

c_light = 2.99792458e8
Bz_clic = 4.0
Bz_cld = 2.0
mchp = 0.139570


def get_decay_type(daughters, gen_part_coll):
    # tau to e= ve vtau (rho --> e+ ve)
    # [11,12,16]
    # tau to mu- vmu vtau (rho --> e+ ve)
    # [13,14,16]
    # tau to rho vtau (rho --> pi+ photon ve)
    # [16,111,211]
    # [16,211,22]
    # tau to pi0 rho vtau
    # [16,111,111,211]
    # tau to 1260 pi0 pi0 vtau
    pdgs = []
    for daugther in daughters:

        pdgs.append(gen_part_coll[daugther].getPDG())
    print("PDGS", pdgs)
    decays = [
        [11, 12, 16],
        [13, 14, 16],
        [16, 111, 211],
        [16, 211],
        [16, 111, 111, 211],
    ]
    decay_check = [
        (set(np.abs(pdgs)) == set(decay)) * (len(pdgs) == len(decay))
        for decay in decays
    ]
    print(decay_check)
    if np.sum(decay_check) == 0:
        # none of the decays considered match
        return 10
    else:
        return np.argmax(decay_check)


def omega_to_pt(omega, isclic):
    if isclic:
        Bz = Bz_clic
    else:
        Bz = Bz_cld
    a = c_light * 1e3 * 1e-15
    return a * Bz / abs(omega)


def track_momentum(trackstate, isclic=True):
    pt = omega_to_pt(trackstate.omega, isclic)
    phi = trackstate.phi
    pz = trackstate.tanLambda * pt
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    p = math.sqrt(px * px + py * py + pz * pz)
    energy = math.sqrt(p * p + mchp * mchp)
    theta = math.acos(pz / p)
    # print(p, theta, phi, energy)
    return p, theta, phi, energy, px, py, pz


def get_genparticle_daughters(i, mcparts):

    p = mcparts[i]
    daughters = p.getDaughters()
    daughter_positions = []
    # for j in range(p.daughters_begin, p.daughters_end):
    #     # print(j, daughters[j].index)
    #     daughter_positions.append(daughters[j].index)
    #     # break
    for daughter in daughters:
        daughter_positions.append(daughter.getObjectID().index)

    return daughter_positions


def find_pandora_cluster_of_hit(hit_index, hit_collection, cluster_collection):

    for index_c, cluster in enumerate(cluster_collection):
        cluster_hits = cluster.getHits()
        cluster_energy = cluster.getEnergy()
        for index_h, hit in enumerate(cluster_hits):
            object_id_hit = hit.getObjectID()
            if (
                hit_index == object_id_hit.index
                and object_id_hit.collectionID == hit_collection
            ):
                pandora_cluster_index = index_c
                cluster_energy_found = cluster_energy
                break
            else:
                pandora_cluster_index = -1
                cluster_energy_found = 0
        if pandora_cluster_index >= 0:
            break
    return pandora_cluster_index, cluster_energy_found


# def check_pandora_pfos(event):
#     pandora_pfo = "PandoraPFOs"
#     pandora_pfos_event = event.get(pandora_pfo)
#     for index, pfo in enumerate(pandora_pfos_event):
#         clusters_pfo = pfo.getClusters()
#         for index_c, cluster in enumerate(clusters_pfo):
#             cluster_hits = cluster.getHits()
#             for index_h, hit in enumerate(cluster_hits):
#         # clusters = pfo.getClusters()
#         # for cluster in clusters:
#         #     print("clusters", dir(cluster))
#         #     print("id", cluster.getObjectID().index)
#         #     cluster_energy = cluster.getEnergy()
#         #     print("cluster energy", cluster_energy)
#         break


def find_pandora_pfo_and_cluster_of_hit(
    hit_index, hit_collection, cluster_collection, pfo_collection
):
    pandora_cluster_index = -1
    pfo_index = -1
    for index_pfo, pfo in enumerate(pfo_collection):
        # print("index pfo ", index_pfo)
        clusters_pfo = pfo.getClusters()
        pfo_energy = pfo.getEnergy()
        for index_c, cluster in enumerate(clusters_pfo):
            # print("index cluster ", index_c)
            cluster_hits = cluster.getHits()
            cluster_energy = cluster.getEnergy()
            cluster_id = cluster.getObjectID().index
            for index_h, hit in enumerate(cluster_hits):
                object_id_hit = hit.getObjectID()
                if (
                    hit_index == object_id_hit.index
                    and object_id_hit.collectionID == hit_collection
                ):
                    pandora_cluster_index = cluster_id
                    cluster_energy_found = cluster_energy
                    pfo_energy_found = pfo_energy
                    pfo_index = index_pfo
                    break
                else:
                    pandora_cluster_index = -1
                    cluster_energy_found = 0
                    pfo_energy_found = 0
                    pfo_index = -1
            if pandora_cluster_index >= 0:
                break
        if pandora_cluster_index >= 0:
            break
    # print("PFO", pfo_index, pfo_energy_found)
    return pandora_cluster_index, cluster_energy_found, pfo_energy_found, pfo_index


def find_pandora_pfo_track(hit_index, hit_collection, pfo_collection):
    pandora_cluster_index = -1
    pandora_pfo_index = -1
    pfo_energy_found = 0
    for index_pfo, pfo in enumerate(pfo_collection):
        tracks_pfo = pfo.getTracks()
        pfo_energy = pfo.getEnergy()
        for index_t, track in enumerate(tracks_pfo):
            # print("index cluster ", index_c)
            track_index = track.getObjectID().index
            track_collection_id = track.getObjectID().collectionID

            if hit_index == track_index and track_collection_id == hit_collection:
                pandora_pfo_index = index_pfo
                pfo_energy_found = pfo_energy
                break
            else:
                pandora_pfo_index = -1
                pfo_energy_found = 0
        if pandora_pfo_index >= 0:
            break
    # print(pandora_cluster_index, pfo_energy_found, pandora_pfo_index)
    return pandora_cluster_index, pfo_energy_found, pandora_pfo_index


def get_genparticle_parents(i, mcparts):

    p = mcparts[i]
    parents = p.getParents()
    # print(p.parents_begin(), p.parents_end())
    parent_positions = []
    # for j in range(p.parents_begin(), p.parents_end()):
    #     # print(j, daughters[j].index)
    #     parent_positions.append(parents[j].index)
    #     # break
    for parent in parents:
        parent_positions.append(parent.getObjectID().index)

    return parent_positions


def find_mother_particle(j, gen_part_coll, index_tau):
    parent_p = j
    counter = 0
    belongs_to_tau = False
    while len(np.reshape(np.array(parent_p), -1)) < 1.5:
        if type(parent_p) == list:
            if len(parent_p) > 0:
                parent_p = parent_p[0]
            else:
                break
        parent_p_r = get_genparticle_parents(
            parent_p,
            gen_part_coll,
        )
        if len(parent_p_r) == 0:
            break
        # print("parent_pr", parent_p_r, index_tau)
        if parent_p_r[0] == index_tau:
            belongs_to_tau = True
        pp_old = parent_p
        counter = counter + 1
        # if len(np.reshape(np.array(parent_p_r), -1)) < 1.5:
        #     print(parent_p, parent_p_r)
        parent_p = parent_p_r
        if belongs_to_tau:
            break
    # if j != pp_old:
    #     print("old parent and new parent", j, pp_old)
    return pp_old, belongs_to_tau


def find_gen_link(
    j,
    id,
    SiTracksMCTruthLink,
    genpart_indexes,
    calo=False,
    gen_part_coll=None,
    index_tau=2,
):
    gen_positions = []
    gen_weights = []
    for i, l in enumerate(SiTracksMCTruthLink):
        rec_ = l.getRec()
        object_id = rec_.getObjectID()
        index = object_id.index
        collectionID = object_id.collectionID
        if index == j and collectionID == id:
            gen_positions.append(l.getSim().getObjectID().index)
            weight = l.getWeight()
            gen_weights.append(weight)
    # print("gen_positions", gen_positions)
    # gen_positions[0] is the MC of the track, now find mother of the MC and check if it is tau_Z
    indices = []
    for i, pos in enumerate(gen_positions):
        if pos in genpart_indexes:
            mother, belongs_to_tau = find_mother_particle(
                genpart_indexes[pos], gen_part_coll, index_tau
            )
            indices.append(mother)
    # print("mother", mother)
    indices += [-1] * (5 - len(indices))
    gen_weights += [-1] * (5 - len(gen_weights))
    # print(gen_positions, indices)
    return indices, gen_weights, belongs_to_tau


def initialize(t):
    event_number = array("i", [0])
    n_hit = array("i", [0])
    n_part = array("i", [0])

    hit_chis = ROOT.std.vector("float")()
    label_true = ROOT.std.vector("float")()
    tau_label = ROOT.std.vector("int")()
    hit_x = ROOT.std.vector("float")()
    hit_y = ROOT.std.vector("float")()
    hit_z = ROOT.std.vector("float")()
    hit_px = ROOT.std.vector("float")()
    hit_py = ROOT.std.vector("float")()
    hit_pz = ROOT.std.vector("float")()
    hit_t = ROOT.std.vector("float")()
    hit_p = ROOT.std.vector("float")()
    hit_e = ROOT.std.vector("float")()
    hit_theta = ROOT.std.vector("float")()
    hit_phi = ROOT.std.vector("float")()
    hit_pandora_cluster_energy = ROOT.std.vector("float")()
    hit_pandora_pfo_energy = ROOT.std.vector("float")()
    ### store here whether track: 0 /ecal: 1/hcal: 2
    hit_type = ROOT.std.vector("int")()
    calohit_col = ROOT.std.vector("int")()

    ### store here the position of the corresponding gen particles associated to the hit
    hit_genlink = ROOT.std.vector(ROOT.std.vector("int"))()

    ### store here the position of the corresponding gen particles associated to the hit in flat format (same info as above but easier to read)
    hit_genlink0 = ROOT.std.vector("int")()
    hit_genlink1 = ROOT.std.vector("float")()
    hit_genlink2 = ROOT.std.vector("float")()
    hit_genlink3 = ROOT.std.vector("float")()
    hit_genlink4 = ROOT.std.vector("float")()

    ## this is the fraction of the energy depoisited by that gen particle in this hit
    hit_genweight0 = ROOT.std.vector("float")()
    hit_genweight1 = ROOT.std.vector("float")()
    hit_genweight2 = ROOT.std.vector("float")()
    hit_genweight3 = ROOT.std.vector("float")()
    hit_genweight4 = ROOT.std.vector("float")()

    ## store here true information
    part_p = ROOT.std.vector("float")()
    part_e = ROOT.std.vector("float")()
    part_theta = ROOT.std.vector("float")()
    part_phi = ROOT.std.vector("float")()
    part_m = ROOT.std.vector("float")()
    part_pid = ROOT.std.vector("float")()
    part_isDecayedInCalorimeter = ROOT.std.vector("float")()
    part_isDecayedInTracker = ROOT.std.vector("float")()

    t.Branch("event_number", event_number, "event_number/I")
    t.Branch("n_hit", n_hit, "n_hit/I")
    t.Branch("n_part", n_part, "n_part/I")

    t.Branch("hit_chis", hit_chis)
    t.Branch("hit_x", hit_x)
    t.Branch("hit_y", hit_y)
    t.Branch("hit_z", hit_z)
    t.Branch("hit_px", hit_px)
    t.Branch("hit_py", hit_py)
    t.Branch("hit_pz", hit_pz)
    t.Branch("hit_t", hit_t)
    t.Branch("hit_p", hit_p)
    t.Branch("hit_e", hit_e)
    t.Branch("hit_theta", hit_theta)
    t.Branch("hit_phi", hit_phi)
    t.Branch("hit_pandora_cluster_energy", hit_pandora_cluster_energy)
    t.Branch("hit_pandora_pfo_energy", hit_pandora_pfo_energy)
    t.Branch("hit_type", hit_type)
    t.Branch("label_true", label_true)
    t.Branch("tau_label", tau_label)
    t.Branch("calohit_col", calohit_col)

    # Create a branch for the hit_genlink_flat
    t.Branch("hit_genlink", hit_genlink)

    t.Branch("hit_genlink0", hit_genlink0)
    t.Branch("hit_genlink1", hit_genlink1)
    t.Branch("hit_genlink2", hit_genlink2)
    t.Branch("hit_genlink3", hit_genlink3)
    t.Branch("hit_genlink4", hit_genlink4)
    t.Branch("hit_genweight0", hit_genweight0)
    t.Branch("hit_genweight1", hit_genweight1)
    t.Branch("hit_genweight2", hit_genweight2)
    t.Branch("hit_genweight3", hit_genweight3)
    t.Branch("hit_genweight4", hit_genweight4)

    t.Branch("part_p", part_p)
    t.Branch("part_e", part_e)
    t.Branch("part_theta", part_theta)
    t.Branch("part_phi", part_phi)
    t.Branch("part_m", part_m)
    t.Branch("part_pid", part_pid)
    t.Branch("part_isDecayedInCalorimeter", part_isDecayedInCalorimeter)
    t.Branch("part_isDecayedInTracker", part_isDecayedInTracker)

    dic = {
        "label_true": label_true,
        "tau_label": tau_label,
        "hit_chis": hit_chis,
        "hit_x": hit_x,
        "hit_y": hit_y,
        "hit_z": hit_z,
        "hit_px": hit_px,
        "hit_py": hit_py,
        "hit_pz": hit_pz,
        "hit_t": hit_t,
        "hit_p": hit_p,
        "hit_e": hit_e,
        "hit_theta": hit_theta,
        "hit_phi": hit_phi,
        "hit_type": hit_type,
        "calohit_col": calohit_col,
        "hit_genlink0": hit_genlink0,
        "hit_genlink1": hit_genlink1,
        "hit_genlink2": hit_genlink2,
        "hit_genlink3": hit_genlink3,
        "hit_genlink4": hit_genlink4,
        "hit_genlink": hit_genlink,
        "hit_genweight0": hit_genweight0,
        "hit_genweight1": hit_genweight1,
        "hit_genweight2": hit_genweight2,
        "hit_genweight3": hit_genweight3,
        "hit_genweight4": hit_genweight4,
        "hit_pandora_cluster_energy": hit_pandora_cluster_energy,
        "hit_pandora_pfo_energy": hit_pandora_pfo_energy,
        "part_p": part_p,
        "part_theta": part_theta,
        "part_phi": part_phi,
        "part_m": part_m,
        "part_e": part_e,
        "part_pid": part_pid,
        "part_isDecayedInCalorimeter": part_isDecayedInCalorimeter,
        "part_isDecayedInTracker": part_isDecayedInTracker,
    }
    return (event_number, n_hit, n_part, dic, t)


def clear_dic(dic):
    for key in dic:
        dic[key].clear()
    return dic


def gen_particles_find(event, debug):
    genparts = "MCParticles"
    genparts_parents = "_MCParticles_parents"
    genparts_daughters = "_MCParticles_daughters"
    # gen_parent_link_indexmc = event.get(genparts_parents)
    # gen_daughter_link_indexmc = event.get(genparts_daughters)
    gen_part_coll = event.get(genparts)
    genpart_indexes_pre = (
        dict()
    )  ## key: index in gen particle collection, value: position in stored gen particle array
    indexes_genpart_pre = (
        dict()
    )  ## key: position in stored gen particle array, value: index in gen particle collection

    n_part_pre = 0
    index_of_tau1 = 0
    index_of_tau2 = 0
    index_of_Z = 0
    for j, part in enumerate(gen_part_coll):
        momentum = part.getMomentum()
        p = math.sqrt(momentum.x**2 + momentum.y**2 + momentum.z**2)

        theta = math.acos(momentum.z / p)
        phi = math.atan2(momentum.y, momentum.x)
        if part.getPDG() == 23:
            daughters = get_genparticle_daughters(
                j,
                gen_part_coll,
            )
            if len(daughters) == 2:
                index_of_Z = j
                index_of_tau1 = daughters[0]
                index_of_tau2 = daughters[1]
        if index_of_Z > 0:
            if j == index_of_tau1:
                # find decay of tau 1
                if (np.abs(part.getPDG()) == 15) and (part.getGeneratorStatus() != 2):
                    daughters = get_genparticle_daughters(
                        j,
                        gen_part_coll,
                    )
                    index_of_tau1 = daughters[0]
                elif (np.abs(part.getPDG()) == 15) and (part.getGeneratorStatus() == 2):
                    ## status 2
                    daughters = get_genparticle_daughters(
                        j,
                        gen_part_coll,
                    )
                    decay_type1 = get_decay_type(daughters, gen_part_coll)
                    print("decay_type1", decay_type1)
            if j == index_of_tau2:
                # find decay of tau 2
                # find decay of tau 1
                if (np.abs(part.getPDG()) == 15) and (part.getGeneratorStatus() != 2):
                    daughters = get_genparticle_daughters(
                        j,
                        gen_part_coll,
                    )
                    index_of_tau2 = daughters[0]
                elif (np.abs(part.getPDG()) == 15) and (part.getGeneratorStatus() == 2):
                    ## status 2
                    daughters = get_genparticle_daughters(
                        j,
                        gen_part_coll,
                    )
                    decay_type2 = get_decay_type(daughters, gen_part_coll)
                    print("decay_type2", decay_type2)
        if debug:
            print(
                "all genparts: N: {}, PID: {}, Q: {}, P: {:.2e}, Theta: {:.2e}, Phi: {:.2e}, M: {:.2e}, X(m): {:.3f}, Y(m): {:.3f}, R(m): {:.3f}, Z(m): {:.3f}, status: {}, parents: {}, daughters: {}, decayed_traacker: {}".format(
                    j,
                    part.getPDG(),
                    part.getCharge(),
                    p,
                    theta,
                    phi,
                    part.getMass(),
                    part.getVertex().x * 1e-03,
                    part.getVertex().y * 1e-03,
                    math.sqrt(part.getVertex().x ** 2 + part.getVertex().y ** 2)
                    * 1e-03,
                    part.getVertex().z * 1e-03,
                    part.getGeneratorStatus(),
                    get_genparticle_parents(
                        j,
                        gen_part_coll,
                    ),
                    get_genparticle_daughters(
                        j,
                        gen_part_coll,
                    ),
                    part.isDecayedInTracker() * 1,
                )
            )

        genpart_indexes_pre[j] = n_part_pre
        indexes_genpart_pre[n_part_pre] = j
        n_part_pre += 1

    return (
        genpart_indexes_pre,
        indexes_genpart_pre,
        n_part_pre,
        gen_part_coll,
        [index_of_tau1, index_of_tau2],
        decay_type1,
        decay_type2,
    )


def store_gen_particles(
    n_part_pre, gen_part_coll, indexes_genpart_pre, dic, n_part, debug, j_tau
):

    genpart_indexes = (
        dict()
    )  ## key: index in gen particle collection, value: position in stored gen particle array
    indexes_genpart = (
        dict()
    )  ## key: position in stored gen particle array, value: index in gen particle collection

    for j in range(n_part_pre):

        part = gen_part_coll[indexes_genpart_pre[j]]
        daughters = get_genparticle_daughters(indexes_genpart_pre[j], gen_part_coll)

        # check if particles has interacted, if it did remove it from the list of gen particles
        # if len(daughters) > 0:
        #    continue
        momentum = part.getMomentum()
        p = math.sqrt(momentum.x**2 + momentum.y**2 + momentum.z**2)
        theta = math.acos(momentum.z / p)
        phi = math.atan2(momentum.y, momentum.x)
        # print(dic["part_p"])
        dic["part_p"].push_back(p)
        dic["part_theta"].push_back(theta)
        dic["part_phi"].push_back(phi)
        dic["part_m"].push_back(part.getMass())
        dic["part_pid"].push_back(part.getPDG())
        dic["part_isDecayedInCalorimeter"].push_back(
            part.isDecayedInCalorimeter() * 1.0
        )
        dic["part_isDecayedInTracker"].push_back(part.isDecayedInTracker() * 1)

        genpart_indexes[indexes_genpart_pre[j]] = n_part[0]
        indexes_genpart[n_part[0]] = indexes_genpart_pre[j]
        n_part[0] += 1

    # if debug:
    #     print("")
    #     # print(genpart_indexes)
    #     for j in range(n_part[0]):
    #         part = gen_part_coll[indexes_genpart[j]]
    #         momentum = part.getMomentum()
    #         p = math.sqrt(momentum.x**2 + momentum.y**2 + momentum.z**2)
    #         theta = math.acos(momentum.z / p)
    #         phi = math.atan2(momentum.y, momentum.x)
    #         print(
    #             "stored genparts: N: {}, PID: {}, P: {:.2e}, Theta: {:.2e}, Phi: {:.2e}, M: {:.2e}".format(
    #                 j, part.getPDG(), p, theta, phi, part.getMass()
    #             )
    #         )
    return dic, genpart_indexes


def store_tracks(
    event,
    debug,
    dic,
    genpart_indexes,
    gen_part_coll,
    n_hit,
    number_of_hist_with_no_genlinks,
    store_pandora_hits=False,
    CLIC="True",
    idx_data=0,
    index_tau=0,
    decay_types=-1,
):
    if CLIC == "True":
        isclic = True
    else:
        isclic = False

    tracks = ("SiTracks_Refitted", 45)
    SiTracksMCTruthLink = "SiTracksMCTruthLink"
    pandora_pfo = "PandoraPFOs"
    pandora_pfos_event = event.get(pandora_pfo)
    gen_track_link_indextr = event.get(SiTracksMCTruthLink)

    track_coll = tracks[0]
    track_collid = tracks[1]

    if debug:
        print("")
    for j, track in enumerate(event.get(track_coll)):
        # check if the track comes from the tau index index_tau
        # if track belongs to particle those mother is taui store otherwise pass
        gen_indices, gen_weights, belongs_to_tau1 = find_gen_link(
            j,
            track.getObjectID().collectionID,
            gen_track_link_indextr,
            genpart_indexes,
            gen_part_coll=gen_part_coll,
            index_tau=index_tau[0],
        )
        gen_indices, gen_weights, belongs_to_tau2 = find_gen_link(
            j,
            track.getObjectID().collectionID,
            gen_track_link_indextr,
            genpart_indexes,
            gen_part_coll=gen_part_coll,
            index_tau=index_tau[1],
        )
        # print("BELONG TO", belongs_to_tau1, belongs_to_tau2)
        if belongs_to_tau1:
            index_tau_ = index_tau[0]
            decay_type = decay_types[0]
            # print("belong to tau 1")
        elif belongs_to_tau2:
            index_tau_ = index_tau[1]
            decay_type = decay_types[1]
            # print("belong to tau 2")
        else:
            decay_type = -1
            index_tau_ = -1
            # print("does not belong to any")

        trackstate = track.getTrackStates()[0]
        referencePoint = trackstate.referencePoint
        x = referencePoint.x
        y = referencePoint.y
        z = referencePoint.z
        R = math.sqrt(x**2 + y**2)
        r = math.sqrt(x**2 + y**2 + z**2)

        chi_s = track.getChi2()

        dic["hit_chis"].push_back(chi_s)
        dic["hit_x"].push_back(x)
        dic["hit_y"].push_back(y)
        dic["hit_z"].push_back(z)
        dic["hit_t"].push_back(trackstate.time)
        dic["label_true"].push_back(decay_type)
        dic["tau_label"].push_back(index_tau_)
        track_mom = track_momentum(trackstate, isclic=isclic)

        dic["hit_p"].push_back(track_mom[0])
        dic["hit_theta"].push_back(track_mom[1])
        dic["hit_phi"].push_back(track_mom[2])
        dic["hit_e"].push_back(-1)
        dic["hit_px"].push_back(track_mom[4])
        dic["hit_py"].push_back(track_mom[5])
        dic["hit_pz"].push_back(track_mom[6])

        dic["hit_type"].push_back(0)  # 0 for tracks at vertex
        dic["calohit_col"].push_back(0)

        if store_pandora_hits == "True":
            (
                pandora_index,
                pandora_pfo_energy,
                pandora_index_pfo,
            ) = find_pandora_pfo_track(
                track.getObjectID().index,
                track.getObjectID().collectionID,
                pandora_pfos_event,
            )
            dic["hit_pandora_cluster_energy"].push_back(0)
            dic["hit_pandora_pfo_energy"].push_back(pandora_index_pfo)
            print(x, y, z, pandora_index_pfo, track_mom[0], chi_s)

        link_vector = ROOT.std.vector("int")()
        for idx in gen_indices:
            link_vector.push_back(idx)

        ngen = len(link_vector)

        if ngen == 0:
            number_of_hist_with_no_genlinks += 1
            if debug:
                print("  -> WARNING: this track with no gen-link")

        dic["hit_genlink"].push_back(
            link_vector
        )  # linked to first particle by default now

        genlink = -1
        if ngen > 0:
            genlink = link_vector[0]

        if len(gen_indices) > 0:
            dic["hit_genlink0"].push_back(gen_indices[0])

        if store_pandora_hits == "True":
            dic["hit_genlink1"].push_back(pandora_index_pfo)
        else:
            if len(gen_indices) > 1:
                dic["hit_genlink1"].push_back(gen_indices[1])
        if store_pandora_hits == "True":
            # print("storing calo hit")
            dic["hit_genlink2"].push_back(pandora_index_pfo)

        else:
            if len(gen_indices) > 2:
                dic["hit_genlink2"].push_back(gen_indices[2])
        if len(gen_indices) > 3:
            dic["hit_genlink3"].push_back(gen_indices[3])
        if len(gen_indices) > 4:
            dic["hit_genlink4"].push_back(gen_indices[4])

        if len(gen_indices) > 0:
            dic["hit_genweight0"].push_back(gen_weights[0])
        if len(gen_indices) > 1:
            dic["hit_genweight1"].push_back(gen_weights[1])
        if len(gen_indices) > 2:
            dic["hit_genweight2"].push_back(gen_weights[2])
        if len(gen_indices) > 3:
            dic["hit_genweight3"].push_back(gen_weights[3])
        if len(gen_indices) > 4:
            dic["hit_genweight4"].push_back(gen_weights[4])

        n_hit[0] += 1

        ## now access trackstate at calo
        trackstate = track.getTrackStates()[3]

        x = trackstate.referencePoint.x
        y = trackstate.referencePoint.y
        z = trackstate.referencePoint.z
        R = math.sqrt(x**2 + y**2)
        r = math.sqrt(x**2 + y**2 + z**2)

        dic["hit_chis"].push_back(chi_s)
        dic["hit_x"].push_back(x)
        dic["hit_y"].push_back(y)
        dic["hit_z"].push_back(z)
        dic["hit_t"].push_back(trackstate.time)
        dic["label_true"].push_back(decay_type)
        dic["tau_label"].push_back(index_tau_)

        track_mom = track_momentum(trackstate, isclic=isclic)

        dic["hit_p"].push_back(track_mom[0])
        dic["hit_theta"].push_back(track_mom[1])
        dic["hit_phi"].push_back(track_mom[2])
        dic["hit_e"].push_back(-1)
        dic["hit_px"].push_back(track_mom[4])
        dic["hit_py"].push_back(track_mom[5])
        dic["hit_pz"].push_back(track_mom[6])

        dic["hit_type"].push_back(1)  # 0 for tracks at calo
        dic["calohit_col"].push_back(0)

        link_vector = ROOT.std.vector("int")()
        for idx in gen_indices:
            link_vector.push_back(idx)

        ngen = len(link_vector)

        if ngen == 0:
            number_of_hist_with_no_genlinks += 1
            if debug:
                print("  -> WARNING: this track with no gen-link")

        dic["hit_genlink"].push_back(
            link_vector
        )  # linked to first particle by default now
        if store_pandora_hits == "True":
            dic["hit_pandora_cluster_energy"].push_back(0)
            dic["hit_pandora_pfo_energy"].push_back(pandora_index_pfo)

        genlink = -1
        if ngen > 0:
            genlink = link_vector[0]

        if len(gen_indices) > 0:
            dic["hit_genlink0"].push_back(gen_indices[0])
        if store_pandora_hits == "True":
            dic["hit_genlink1"].push_back(pandora_index_pfo)
        else:
            if len(gen_indices) > 1:
                dic["hit_genlink1"].push_back(gen_indices[1])
        if store_pandora_hits == "True":
            # print("storing calo hit")
            # print("storing pandora pfo track", pandora_index_pfo)
            dic["hit_genlink2"].push_back(pandora_index_pfo)
        else:
            if len(gen_indices) > 2:
                dic["hit_genlink2"].push_back(gen_indices[2])
        if len(gen_indices) > 3:
            dic["hit_genlink3"].push_back(gen_indices[3])
        if len(gen_indices) > 4:
            dic["hit_genlink4"].push_back(gen_indices[4])

        if len(gen_indices) > 0:
            dic["hit_genweight0"].push_back(gen_weights[0])
        if len(gen_indices) > 1:
            dic["hit_genweight1"].push_back(gen_weights[1])
        if len(gen_indices) > 2:
            dic["hit_genweight2"].push_back(gen_weights[2])
        if len(gen_indices) > 3:
            dic["hit_genweight3"].push_back(gen_weights[3])
        if len(gen_indices) > 4:
            dic["hit_genweight4"].push_back(gen_weights[4])

        n_hit[0] += 1

    return n_hit, dic, number_of_hist_with_no_genlinks


def store_calo_hits(
    event,
    debug,
    dic,
    n_hit,
    genpart_indexes,
    gen_part_coll,
    number_of_hist_with_no_genlinks,
    store_pandora_hits,
    CLIC,
    idx_data,
    index_tau=0,
    decay_types=-1,
):
    ## calo stuff
    ecal_barrel = ("ECALBarrel", 46)
    ecal_endcap = ("ECALEndcap", 47)
    print("using CLIC dataset", CLIC)
    if CLIC == "True":
        ecal_other = ("ECALOther", 48)
    hcal_barrel = ("HCALBarrel", 49)
    hcal_endcap = ("HCALEndcap", 50)
    hcal_other = ("HCALOther", 51)
    gen_calo_links0 = "CalohitMCTruthLink"
    pandora_clusters = "PandoraClusters"
    pandora_pfo = "PandoraPFOs"
    gen_calohit_link_indexhit = event.get(gen_calo_links0)
    pandora_clusters_event = event.get(pandora_clusters)
    pandora_pfos_event = event.get(pandora_pfo)
    print("checking clic again", CLIC)
    if CLIC == "True":
        print("here")
        calohit_collections = [
            ecal_barrel[0],
            hcal_barrel[0],
            ecal_endcap[0],
            hcal_endcap[0],
            ecal_other[0],
            hcal_other[0],
        ]
    else:
        print("here2")
        calohit_collections = [
            ecal_barrel[0],
            hcal_barrel[0],
            ecal_endcap[0],
            hcal_endcap[0],
            hcal_other[0],
        ]

    total_calohit_e = 0
    total_calohit_ = np.zeros(11)
    total_calohit_e_pandora = 0
    total_calohit_pandora = np.zeros(15)
    for calohit_col_index, calohit_coll in enumerate(calohit_collections):
        if debug:
            print("")
        for j, calohit in enumerate(event.get(calohit_coll)):
            # check if it belongs to tau i
            hit_collection = calohit.getObjectID().collectionID
            gen_indices, gen_weights, belongs_to_tau1 = find_gen_link(
                j,
                hit_collection,
                gen_calohit_link_indexhit,
                genpart_indexes,
                calo=True,
                gen_part_coll=gen_part_coll,
                index_tau=index_tau[0],
            )
            gen_indices, gen_weights, belongs_to_tau2 = find_gen_link(
                j,
                hit_collection,
                gen_calohit_link_indexhit,
                genpart_indexes,
                calo=True,
                gen_part_coll=gen_part_coll,
                index_tau=index_tau[1],
            )

            # print("BELONG TO", belongs_to_tau1, belongs_to_tau2)
            if belongs_to_tau1:
                index_tau_ = index_tau[0]
                decay_type = decay_types[0]
                # print("belong to tau 1")
            elif belongs_to_tau2:
                index_tau_ = index_tau[1]
                decay_type = decay_types[1]
                # print("belong to tau 2")
            else:
                decay_type = -1
                index_tau_ = -1
                # print("does not belong to any")

            position = calohit.getPosition()
            x = position.x
            y = position.y
            z = position.z
            R = math.sqrt(x**2 + y**2)
            r = math.sqrt(x**2 + y**2 + z**2)

            dic["hit_chis"].push_back(0)
            dic["hit_x"].push_back(x)
            dic["hit_y"].push_back(y)
            dic["hit_z"].push_back(z)
            dic["hit_t"].push_back(calohit.getTime())
            dic["hit_p"].push_back(-1)
            dic["hit_e"].push_back(calohit.getEnergy())
            dic["label_true"].push_back(decay_type)
            dic["tau_label"].push_back(index_tau_)
            dic["hit_px"].push_back(0.0)
            dic["hit_py"].push_back(0.0)
            dic["hit_pz"].push_back(0.0)
            theta = math.acos(z / r)
            phi = math.atan2(y, x)

            dic["hit_theta"].push_back(theta)
            dic["hit_phi"].push_back(phi)

            htype = 2  # 2 if ECAL, 3 if HCAL
            if "HCAL" in calohit_coll:
                htype = 3

            dic["hit_type"].push_back(htype)  # 0 for calo hits
            dic["calohit_col"].push_back(calohit_col_index + 1)

            # print(gen_indices)
            link_vector = ROOT.std.vector("int")()
            for idx in gen_indices:
                link_vector.push_back(idx)
            # if j > 3:
            #     break

            ngen = len(link_vector)

            if ngen == 0:
                number_of_hist_with_no_genlinks += 1
                # if debug:
                #    print("  -> WARNING: this calo hit has no gen-link")

            dic["hit_genlink"].push_back(
                link_vector
            )  # linked to first particle by default now

            if gen_indices[0] == 4:
                print(gen_indices)
            genlink = -1
            if ngen > 0:
                genlink = link_vector[0]
            if store_pandora_hits == "True":
                # print("looking for calo hit")
                (
                    pandora_cluster,
                    pandora_cluster_energy,
                    pfo_energy,
                    pandora_pfo_index,
                ) = find_pandora_pfo_and_cluster_of_hit(
                    j, hit_collection, pandora_clusters_event, pandora_pfos_event
                )
                dic["hit_pandora_cluster_energy"].push_back(pandora_cluster_energy)
                dic["hit_pandora_pfo_energy"].push_back(pandora_pfo_index)

            if len(gen_indices) > 0:
                dic["hit_genlink0"].push_back(gen_indices[0])
            if store_pandora_hits == "True":
                # print("storing calo hit")
                dic["hit_genlink1"].push_back(pandora_cluster)
            else:
                if len(gen_indices) > 1:
                    dic["hit_genlink1"].push_back(0)
            if store_pandora_hits == "True":
                # print("storing calo hit")
                # print("storing pandora pfo", pandora_pfo_index)
                dic["hit_genlink2"].push_back(pandora_pfo_index)
            else:
                if len(gen_indices) > 2:
                    dic["hit_genlink2"].push_back(0)
            if len(gen_indices) > 3:
                dic["hit_genlink3"].push_back(gen_indices[1])
            if len(gen_indices) > 4:
                dic["hit_genlink4"].push_back(gen_indices[4])

            if len(gen_indices) > 0:
                dic["hit_genweight0"].push_back(gen_weights[0])
            if len(gen_indices) > 1:
                dic["hit_genweight1"].push_back(gen_weights[1])
            if len(gen_indices) > 2:
                dic["hit_genweight2"].push_back(gen_weights[2])
            if len(gen_indices) > 3:
                dic["hit_genweight3"].push_back(gen_weights[3])
            if len(gen_indices) > 4:
                dic["hit_genweight4"].push_back(gen_weights[4])

            n_hit[0] += 1

    return (
        n_hit,
        dic,
        total_calohit_,
        number_of_hist_with_no_genlinks,
        total_calohit_pandora,
    )
