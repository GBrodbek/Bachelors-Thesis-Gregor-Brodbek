#!/usr/bin/env python

import numpy as np
import sys
import ROOT

variables = {
    "event_number": (0, 1000, None, None),   # histogram options, start, end, binsize, yscale ('ylog' for log scale)
    "n_hit": (0, 3000, None, None),
    "n_part": (0, 10000, None, 'ylog'),
    "hit_chis": (0, 500, None, 'ylog'),
    "hit_x": (-4000, 4000, None, None),
    "hit_y": (-4000, 4000, None, None),
    "hit_z": (-4000, 4000, None, None),
    "hit_px": (-50, 50, None, 'ylog'),
    "hit_py": (-50, 50, None, 'ylog'),
    "hit_pz": (-50, 50, None, 'ylog'),
    "hit_t": (-2, 15, None, 'ylog'),
    "hit_p": (-10, 60, None, 'ylog'),
    "hit_e": (-2, 6, None, 'ylog'),
    "hit_theta": (-1, 4, None, None),
    "hit_phi": (-4, 4, None, None),
    "hit_pandora_cluster_energy": (None, None, None, None),
    "hit_pandora_pfo_energy": (None, None, None, None),
    "hit_type": (-0.5, 4.5, 1, 'ylog'),
    "label_true": (-0.5, 4.5, 1, None),
    "tau_label": (0, 35, 1, None),
    "calohit_col": (-0.5, 5.5, 1, None),
    "hit_genlink": (-2, 15, 0.5, 'ylog'),
    "hit_genlink0": (0, 40, 1, 'ylog'),
    "hit_genlink1": (-2, 10, 1, 'ylog'),
    "hit_genlink2": (-2, 2, 1, 'ylog'),
    "hit_genlink3": (0, 45, 1, 'ylog'),
    "hit_genlink4": (-1.5, 0.5, 1, 'ylog'),
    "hit_genweight0": (0, 6, None, 'ylog'),
    "hit_genweight1": (-3, 3, None, 'ylog'),
    "hit_genweight2": (-3, 3, None, 'ylog'),
    "hit_genweight3": (-2, 0, 0.5, None),
    "hit_genweight4": (-2, 1, 0.5, None),
    "part_p": (0, 50, None, 'ylog'),
    "part_e": (None, None, None, None),
    "part_theta": (-1, 4, None, None),
    "part_phi": (-4, 4, None, None),
    "part_m": (0, 200, None, 'ylog'),
    "part_pid": (-100, 2500, None, None),
    "part_isDecayedInCalorimeter": (-0.5, 1.5, 1, None),
    "part_isDecayedInTracker": (-0.5, 1.5, 1, None)
}

if len(sys.argv) != 2:
    print("Usage: python makeHistogramsFromRoot.py <root_file>")
    sys.exit(1)

root_file = sys.argv[1]
in_file = ROOT.TFile.Open(root_file, "READ")
in_tree = in_file.Get("events;1")

var_list = list(variables.keys())

for var in var_list:
    start, end, binsize, yscale = variables[var]                    # get histogram options
    if binsize is None:                                             # set nbins to 100 if not specified
        nbins = 100
    else:                                                           #  otherwise calculate number of bins
        nbins = int((end - start) / binsize)
    hist_name = f"{var}_hist"                                       # histogram name
    in_tree.Draw(f"{var}>>{hist_name}({nbins}, {start}, {end})")    # draw histogram
    hist = ROOT.gDirectory.Get(hist_name)                           # get histogram

    canv = ROOT.TCanvas(var, var, 600, 600)                         # create canvas
    if yscale == 'ylog':                                            # set y scale to log if specified
        canv.SetLogy()
        canv.Update()
    canv.cd()
    hist.Draw()
    canv.SaveAs(f"histograms/signal/{var}_hist.pdf")                # save histogram as pdf

in_file.Close()