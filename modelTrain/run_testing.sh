#!/usr/bin/env bash

# Set HOME to current job directory
HOME=$_CONDOR_JOB_IWD
MODELNAME=run16.ckpt
CLUSTER_ID=$1
PROCESS_ID=$2

cd ${HOME}
mkdir -p tmp/

# Copy files into job
(
    source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-ubuntu2004-gcc9-opt/setup.sh
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/newTrainingFiles/signal/output_1149668_{50..99}.root tmp/
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/newTrainingFiles/zqq/background_1160162_{20..39}.root tmp/
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/newTrainingFiles/bhabha/newlabels/bhabha_scattering_1365720_{0..9}.root tmp/
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/modelsaves/${MODELNAME} tmp/
)

# directory to save model weights, that get transferred back
mkdir -p tmp/modelsaves/

# extract tar file
tar -xzf scriptForTraining.tar.gz

# login to wandb to track model training
export WANDB_API_KEY=  # use your API key for wandb
wandb login

# Run testing
cd PID_GNN
python3 -m src.train_lightning1 --data-test  ${HOME}/tmp/output_1149668_{50..99}.root ${HOME}/tmp/background_1160162_{20..39}.root ${HOME}/tmp/bhabha_scattering_1365720_{0..9}.root  --data-config config_files/config_hit_tracks_tau_predict.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/  --num-workers 0 --gpus 1   --batch-size  60 --start-lr 1e-3 --num-epochs 10  --fetch-step 0.02 --log-wandb --wandb-displayname run16_testrun --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749 --load-model-weights ${HOME}/tmp/${MODELNAME}  --predict
