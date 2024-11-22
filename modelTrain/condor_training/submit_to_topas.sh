#!/bin/bash

# make sure to have the following directories to log the job
mkdir -p logs/{err,out,log}

# remove old files
find logs/err/ -type f -mmin +3 -delete
find logs/log/ -type f -mtime +2 -delete
find logs/out/ -type f -mtime +0.5 -delete

# rm old zipped training scripts
if [ -f scriptForTraining.tar.gz ] ; then
    rm scriptForTraining.tar.gz
fi

# remove the old job submission file and executable
rm jobForTraining.cfg
rm run_training.sh

# freshly zip the training scripts, so it contains all changes
cp -r /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/PID_GNN .
tar -czf scriptForTraining.tar.gz PID_GNN/
rm -r PID_GNN/

# copy the configuration file for the job to the current directory
cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/jobForTraining.cfg .
cp /work/gbrodbek/FCC_fullsim/FullSim_TauID/modelTrain/run_training.sh .

# submit the job to condor
condor_submit jobForTraining.cfg

# condor_watch_q