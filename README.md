# Bachelor's Thesis Gregor Brodbek

This repository contains all scripts and files of the Bachelor's Thesis "Tau Reconstruction at FCC-ee using Machine Learning based on Full Detector Simulation" by Gregor Brodbek.

Everything inside the directory modelTrain/PID_GNN is adapted from [Dolores Garcia's work](https://github.com/doloresgarcia/PID_GNN).

<!--
## Quick links
- [Generation of Full Detector Simulation Samples](#Generation-of-Full-Detector-Simulation-Samples)
- [Training the Model](#Training-the-Model)
- [Testing the Model](#Testing-the-Model)
- [Changing Parameters of the Training](#Changing-Parameters-of-the-Training)
- [Plots and Confusion Matrix](#Plots-and-Confusion-Matrix)
-->

## Generation of Full Detector Simulation Samples

The event generation chain looks like this:

1) Source the key4hep nightlie build. One of the functions in the treemaker wasn't working with the newer versions, so I was using the version 2024-09-21.
2) Monte Carlo simulation with Pythia8
3) Detector simulation with geant4
4) Pandora reconstruction
5) Treemaker by Dolores

I wrote a [script](./files_for_generation_chain/condorSubmission/submitFullsim.sh), that automatically submits the whole simulation process to HTCondor at ETP. Different Pythia cards for different processes can be found [here](./files_for_generation_chain/Zcards). Also Xunwu made a [repository](https://github.com/zuoxunwu/FullSim_TauID), that explains the whole generation process in more detail.

You can add more decay modes in this [function](./files_for_generation_chain/pftree_maker_from_dolores/tree_tools_tautau.py#L16C1-L50C38).


## Training the Model

To start the training, the docker container from Dolores `docker://dologarcia/gatr:v0` needs to be setup. ETP users can use this [script](./modelTrain/startContainer.sh) to start the container, that was setup by Jan.
The command to start the training looks like this:

```python3 -m src.train_lightning1 --data-train ${HOME}/tmp/output_1149668_{0..49}.root ${HOME}/tmp/background_1160162_{0..19}.root ${HOME}/tmp/bhabha_scattering_1365720_{0..9}.root --data-config config_files/config_hit_tracks_tau.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/ --num-workers 0 --gpus 1 --batch-size 15 --start-lr 1e-3 --num-epochs 10  --fetch-step 0.1 --log-wandb --wandb-displayname run19 --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749```

`--data-train` takes the input files in the root format of the treemaker

`--data-config` [config file](./modelTrain/PID_GNN/config_files)

`-clust` and `-clust_dim` not sure, I just left it the way Dolores sent me the command

`--network-config` the model that is trained. [Original model of Dolores](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho_original.py), [Model with my changes](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py)

`--model-prefix` the model weights get saved here after the training is done

`--num-workers` again not sure, left it as it was

`--gpus` number or amount of gpus that is used, I think this was not yet implemented and hardcoded somewhere though

`--batch-size` batch size

`--start-lr` starting learning rate, but its currently still hardcoded [here](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L422C67-L422C74) as far as I can tell

`--num-epochs` number of epochs

`--fetch-step` not sure

`--log-wandb`, `--wandb-displayname`, `--wandb-projectname`, `--wandb-entity` These are for logging everything on [WandB](https://wandb.ai/gbrodbek-kit4749/topas_logs?nw=nwusergbrodbek)


## Testing the Model

The command for the testruns is similar to the training run:

```python3 -m src.train_lightning1 --data-test  ${HOME}/tmp/output_1149668_{50..99}.root ${HOME}/tmp/background_1160162_{20..39}.root ${HOME}/tmp/bhabha_scattering_1365720_{0..9}.root  --data-config config_files/config_hit_tracks_tau_predict.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/  --num-workers 0 --gpus 1   --batch-size  60 --start-lr 1e-3 --num-epochs 10  --fetch-step 0.02 --log-wandb --wandb-displayname run16_testrun --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749 --load-model-weights ${HOME}/tmp/${MODELNAME}  --predict```

`--predict` is needed to put the script in the test mode

`--load-model-weights` loads the weights that were achieved in the training

Note that another config file is needed for the test runs.


For the training and testing, I again used a [script](./modelTrain/condor_training/submit_to_topas.sh), that automatically sends everything to HTCondor and TOpAS.


## Changing Parameters of the Training

- Change [start learning rate](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L422C67-L422C74)
- Modify [class specific weights](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L99C4-L127C1) to normalize the ratios of samples that are used per class
- Change number of classes:
  - Adapt num_classes in [1](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L303C58-L303C71), [2](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L248C58-L248C71) and in the readout [MLP](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L96C44-L96C46) (the back number).
  - Adapt the [index mapping](./modelTrain/PID_GNN/src/dataset/functions_graph.py#L217C1-L219C10), to the classes that should be considered in the training. Index 10 gets removed before training
  - The [tensors in the loss weight function](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L118C9-L120C76) must have the same length as the amount of labels/classes in the training
  - Any additional classes must also be added [here](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L308C13-L319C60)
- Changes to the GATr Model can be made [here](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L78C9-L88C10)
 
## Plots and Confusion Matrix

At the end of each validation or prediction step, this [function](./modelTrain/PID_GNN/src/models/Gatr_pf_e_tau_rho.py#L375C1-L406C44) is executed and creates a confusion matrix and ROC curves, that can be seen on WandB. For everyone interested on how to make the plots I used in the thesis, check the [plots file](./plots).
