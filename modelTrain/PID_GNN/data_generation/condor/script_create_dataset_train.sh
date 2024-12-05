#!/bin/bash

# python submit_jobs_train.py --config config_spread_300424.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/300424/dr_01/40_50/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/300424/dr_01/40_50/ --njobs 2000 --nev 100 --queue workday


# python submit_jobs_train.py --config config_pion0.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/single_particles_flat/pion0_v3/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/single_particles_flat/pion_v3/ --idx 1 --njobs 200 --nev 100 --queue workday

# python submit_jobs_train.py --config config_pion.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/single_particles_flat/pion_v3/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/single_particles_flat/pion_v3/ --idx 0 --njobs 200 --nev 100 --queue workday

# python submit_jobs_train.py --config config_electron.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/single_particles_flat/electron_v3/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/single_particles_flat/electron_v3/ --idx 2 --njobs 200 --nev 100 --queue workday

# python submit_jobs_train.py --config config_muon.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/single_particles_flat/muon_v3/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/single_particles_flat/muon_v3/ --idx 3 --njobs 200 --nev 100 --queue workday

# python submit_jobs_train.py --config config_resonance.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/single_particles_flat/rho_v3/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/single_particles_flat/rho_v3/ --idx 4 --njobs 200 --nev 100 --queue workday

python submit_jobs_train.py --config config_tau.gun --outdir /eos/experiment/fcc/ee/datasets/mlpf/CLD/train/Z_tautau_v8/ --condordir /eos/experiment/fcc/ee/datasets/mlpf/condor/train/Z_tautau_v6/ --idx 5 --njobs 3000 --nev 100 --queue workday

