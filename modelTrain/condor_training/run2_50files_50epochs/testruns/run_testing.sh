#!/usr/bin/env bash

# Set HOME to current job directory
HOME=$_CONDOR_JOB_IWD

cd ${HOME}

# Copy files into job
(
    source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-ubuntu2004-gcc9-opt/setup.sh
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/trainingFiles/output_1279601_{1..10}.root tmp/
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/modelsaves/final_save_50files10epochs.ckpt tmp/
)

# directory to save model weights, that get transferred back
mkdir -p tmp/modelsaves

# extract tar file
tar -xzf scriptForTraining.tar.gz

# login to wandb to track model training
export WANDB_API_KEY=ef88c6e1260343f280284ed9716c1f4bb76d76b1  # use your API key for wandb
wandb login

# Run testing
cd PID_GNN
python3 -m src.train_lightning1 --data-test  ${HOME}/tmp/output_1279601_{1..10}.root  --data-config config_files/config_hit_tracks_tau_predict.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/tmp/modelsaves/  --num-workers 0 --gpus 1   --batch-size  32 --start-lr 1e-3 --num-epochs 10  --fetch-step 0.02 --log-wandb --wandb-displayname 50files_testing_with_10files --wandb-projectname topas_logs --wandb-entity gbrodbek-kit4749 --load-model-weights ${HOME}/tmp/final_save_50files10epochs.ckpt  --predict