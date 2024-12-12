#!/usr/bin/env bash

# Set HOME to current job directory
HOME=$_CONDOR_JOB_IWD
MODELNAME=run3_finalsave.ckpt

cd ${HOME}
mkdir -p tmp/

# Copy files into job
(
    source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-ubuntu2004-gcc9-opt/setup.sh
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/newTrainingFiles/output_1149668_{0..50}.root tmp/
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/newTrainingFiles/background_1160162_{0..50}.root tmp/
    # xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/modelsaves/${MODELNAME} tmp/                 # for further training a saved model

)

# directory to save model weights, that get transferred back
mkdir -p tmp/modelsaves

# extract tar file
tar -xzf scriptForTraining.tar.gz

# login to wandb to track model training
export WANDB_API_KEY=ef88c6e1260343f280284ed9716c1f4bb76d76b1  # use your API key for wandb
wandb login

# Run training
cd PID_GNN

#  from the beginning
python3 -m src.train_lightning1 --data-train ${HOME}/tmp/output_1149668_{0..50}.root ${HOME}/tmp/background_1160162_{0..50}.root --data-config config_files/config_hit_tracks_tau.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/ --num-workers 25 --gpus 1 --batch-size 25 --start-lr 1e-3 --num-epochs 50  --fetch-step 0.1 --log-wandb --wandb-displayname run5_newWithBackground --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749

# continue training from a saved model
# python3 -m src.train_lightning1 --data-train ${HOME}/tmp/output_1149668_{0..50}.root ${HOME}/tmp/background_1160162_{0..50}.root  --data-config config_files/config_hit_tracks_tau.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/ --num-workers 0 --gpus 1 --batch-size 30 --start-lr 1e-3 --num-epochs 50  --fetch-step 0.1 --log-wandb --wandb-displayname newfiles100epochs50 --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749 --load-model-weights ${HOME}/tmp/${MODELNAME}