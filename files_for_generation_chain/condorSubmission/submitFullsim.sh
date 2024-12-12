#!/usr/bin/bash

# This script is used to submit the fullsim jobs to the condor batch system.

echo "Which process do you want to simulate? (0: Z -> tautau, 1: Z -> ud, 2: Z -> ss, 3: Z -> cc, 4: Z -> bb, 5: Z -> qq, 6: bhabha scattering)"
read PROCESS

case $PROCESS in
    0) PROCESS="Z_to_tautau" ;;
    1) PROCESS="Z_to_ud" ;;
    2) PROCESS="Z_to_ss" ;;
    3) PROCESS="Z_to_cc" ;;
    4) PROCESS="Z_to_bb" ;;
    5) PROCESS="Z_to_qq" ;;
    6) PROCESS="bhabha_scattering" ;;
    *) 
        echo "Invalid choice, exiting."
        exit 1
        ;;
esac

echo "How many files (1000 events each) do you want to simulate? (max. 300)"
read NUM_FILES

if [ $NUM_FILES -gt 300 ]; then
    echo "Invalid number of files, exiting."
    exit 1
fi

echo "Where do you want to save the output files? (0: Gregors standard directory, don't use this option unless you are Gregor)"
read SAVE_DIR

# check if directory exists, give my standard directory for =0 (just for my own convenience :))
if [ $SAVE_DIR -eq 0 ]; then
    SAVE_DIR="/ceph/gbrodbek/data/"
elif [ ! -d $SAVE_DIR ]; then
    echo "Directory does not exist, please create directory first."
    exit 1
fi

echo "Simulating ${NUM_FILES} files for process ${PROCESS} ($((1000*NUM_FILES)) events), saving output to ${SAVE_DIR}. Continue? (y/n)"
read CONTINUE

if [ $CONTINUE != "y" ]; then
    echo "Exiting."
    exit 1
fi

# create directories for data storage and condor logs
mkdir -p ${SAVE_DIR}/${PROCESS}/{outputFiles,temporaryFiles,logs/{log,err,out}}

# submit jobs to condor
condor_submit /work/gbrodbek/FCC_fullsim/FullSim_TauID/files_for_generation_chain/condorSubmission/jobConfigFullsim.cfg -a "WHICH_PROCESS=${PROCESS}" -a "NUM_FILES=${NUM_FILES}" -a "SAVE_DIR=${SAVE_DIR}"

condor_watch_q