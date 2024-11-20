#!/usr/bin/env bash

#if [[ -z "${USE_USER}" ]]; then
#    echo "USE_USER not set. Please source the setup.sh"
#    exit 1
#fi

# Set HOME to current job directory
HOME=$_CONDOR_JOB_IWD

# create new python environment
cd ${HOME}/tmp
# Set up venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pip --upgrade
# install pytorch
#python3 -m pip install torch==1.10.1 torchvision==0.11.2 torchaudio==0.10.1
cd ${HOME}

# Copy files into job
(
    source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
    xrdcp -r root://ceph-node-j.etp.kit.edu://gbrodbek/trainingFiles/
)

# extract tar file
tar -xzf scriptForTraining.tar.gz
# Run training
cd PID_GNN
python3 -m src.train_lightning1 --data-train ${HOME}/trainingFiles/output_1279601_{1..2}.root  --data-config config_files/config_hit_tracks_tau.yaml -clust -clust_dim 3 --network-config src/models/wrapper/example_mode_gatr_e.py --model-prefix ${HOME}/ --num-workers 0 --gpus 0   --batch-size 16  --start-lr 1e-3 --num-epochs 10  --fetch-step 0.1 --log-wandb --wandb-displayname run_model --wandb-projectname test_logs --wandb-entity gbrodbek-kit4749