#!/bin/bash

if [ "$1" == "test" ]; then
    train_mode=false
elif [ "$1" == "train" ]; then
    train_mode=true
else
    echo "Please provide a mode: 'test' or 'train'"
    exit 1
fi

# make sure to have the following directories to log the job
mkdir -p logs/{err,out,log}

# remove old files
find logs/err/ -type f -mtime +2 -delete
find logs/log/ -type f -mtime +2 -delete
find logs/out/ -type f -mtime +2 -delete

# rm old zipped training scripts
rm -f scriptForTraining.tar.gz

# remove the old job submission file and executable
rm -f jobForTraining.cfg
rm -f run_training.sh
rm -f jobForTesting.cfg
rm -f run_testing.sh

# freshly zip the training scripts, so it contains all changes
cp -r /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/PID_GNN .
tar -czf scriptForTraining.tar.gz PID_GNN/
rm -r PID_GNN/

if [ "$train_mode" = true ]; then
    # copy the configuration file and executable for training to the current directory
    cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/jobForTraining.cfg .
    cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/run_training.sh .
    # submit the job to condor
    condor_submit jobForTraining.cfg
else
    # copy the configuration file and executable for testing to the current directory
    cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/jobForTesting.cfg .
    cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/run_testing.sh .
    # submit the job to condor
    condor_submit jobForTesting.cfg
fi

condor_watch_q
