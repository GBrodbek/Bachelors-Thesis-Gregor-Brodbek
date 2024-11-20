import sys
import math
import ROOT
from array import array
from ROOT import TFile, TTree
import numpy as np
from podio import root_io
import edm4hep
from tree_tools_tautau import (
    initialize,
    clear_dic,
    gen_particles_find,
    store_gen_particles,
    store_tracks,
    store_calo_hits,
)

# TODO
# is last track state position at calo?
# Bz should be stored in the in the tree
# should allow for multiple gen links to hit (probablyhas to be done in the previous edm4hep formation stage)

debug = False
"""
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

python scripts/make_pftree_clic.py /afs/cern.ch/work/s/selvaggi/private/particleflow/fcc/out_reco_edm4hep.root tree.root 

"""

## global params
CALO_RADIUS_IN_MM = 1500

if len(sys.argv) < 2:
    print(" Usage: make_pftree.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
store_pandora_hits = sys.argv[3]

print("will store calo hits", store_pandora_hits)
CLIC = sys.argv[4]
print("is it CLIC", CLIC)
indx_data = int(sys.argv[5])
print("adding this label to data: ", indx_data)

reader = root_io.Reader(input_file)

out_root = TFile(output_file, "RECREATE")
t = TTree("events", "pf tree lar")
event_number, n_hit, n_part, dic, t = initialize(t)

event_number[0] = 0
for i, event in enumerate(reader.get("events")):
    number_of_hist_with_no_genlinks = 0
    (
        genpart_indexes_pre,
        indexes_genpart_pre,
        n_part_pre,
        gen_part_coll,
        index_Z,
        decay_type1,
        decay_type2,
    ) = gen_particles_find(event, debug)
    # clear all the vectors
    # either go twice through the event or store two different events for each...
    # for j_tau in range(0, 2):
    print(index_Z, decay_type1, decay_type2)
    index_taus = index_Z
    decay_types = [decay_type1, decay_type2]

    dic = clear_dic(dic)
    n_part[0] = 0

    dic, genpart_indexes = store_gen_particles(
        n_part_pre,
        gen_part_coll,
        indexes_genpart_pre,
        dic,
        n_part,
        debug,
        index_taus,
    )

    n_hit[0] = 0

    n_hit, dic, number_of_hist_with_no_genlinks = store_tracks(
        event,
        debug,
        dic,
        genpart_indexes,
        gen_part_coll,
        n_hit,
        number_of_hist_with_no_genlinks,
        store_pandora_hits,
        CLIC,
        indx_data,
        index_tau=index_taus,
        decay_types=decay_types,
    )

    (
        n_hit,
        dic,
        total_calohit_,
        number_of_hist_with_no_genlinks,
        total_calohit_pandora,
    ) = store_calo_hits(
        event,
        debug,
        dic,
        n_hit,
        genpart_indexes,
        gen_part_coll,
        number_of_hist_with_no_genlinks,
        store_pandora_hits,
        CLIC,
        indx_data,
        index_tau=index_taus,
        decay_types=decay_types,
    )

    if n_hit[0] <= number_of_hist_with_no_genlinks:
        print(
            "  --> WARNING: all hists in this event have no gen link associated or simply no hits, skipping event"
        )
    else:
        event_number[0] += 1
        t.Fill()

t.SetDirectory(out_root)
t.Write()
