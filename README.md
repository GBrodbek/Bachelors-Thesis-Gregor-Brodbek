# Bachelor's Thesis Gregor Brodbek

This repository contains all scripts and files of the Bachelor's Thesis "Tau Reconstruction at FCC-ee using Machine Learning based on Full Detector Simulation" by Gregor Brodbek.

Everything inside the directory modelTrain/PID_GNN is adapted from [Dolores Garcia's work](https://github.com/doloresgarcia/PID_GNN).


## Generation of Full Detector Simulation Samples

The event generation chain looks like this:

1) Source the key4hep nightlie build. One of the functions in the treemaker wasn't working with the newer versions, so I was using the version 2024-09-21.
2) Monte Carlo simulation with Pythia8
3) Detector simulation with geant4
4) Pandora reconstruction
5) Treemaker by Dolores

I wrote a [script](./files_for_generation_chain/condorSubmission/submitFullsim.sh), that automatically submits the whole simulation process to HTCondor at ETP. Different Pythia cards for different processes can be found [here](./files_for_generation_chain/Zcards). Also Xunwu made a [repository](https://github.com/zuoxunwu/FullSim_TauID), that explains the whole generation process in more detail.


## Training the Model

The command to start the training looks like this:

```python3 -m src.train_lightning1 --data-train ${HOME}/tmp/output_1149668_{0..49}.root ${HOME}/tmp/background_1160162_{0..19}.root ${HOME}/tmp/bhabha_scattering_1365720_{0..9}.root --data-config config_files/config_hit_tracks_tau.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/ --num-workers 0 --gpus 1 --batch-size 15 --start-lr 1e-3 --num-epochs 10  --fetch-step 0.1 --log-wandb --wandb-displayname run19 --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749```

`--data-train` takes the input files in the root format of the treemaker
`--data-config` config file
`-clust` and `-clust_dim` not sure, I just left it the way Dolores sent me the command
`--network-config` the model that is trained. [Original model of Dolores](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho_original.py), [Model with my changes](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py)
`--model-prefix` the model parameters get saved here after the training is done
`--num-workers` again not sure, left it as it was
`--gpus` number or amount of gpus that is used, I think this was not yet implemented and hardcoded somewhere though
`--batch-size` batch size
`--start-lr` starting learning rate, but its currently still hardcoded [here](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L422C67-L422C74) as far as I can tell
`--num-epochs` number of epochs
`--fetch-step` not sure
`--log-wandb`, `--wandb-displayname`, `--wandb-projectname`, `--wandb-entity` These are for logging everything on [WandB](https://wandb.ai/gbrodbek-kit4749/topas_logs?nw=nwusergbrodbek)
