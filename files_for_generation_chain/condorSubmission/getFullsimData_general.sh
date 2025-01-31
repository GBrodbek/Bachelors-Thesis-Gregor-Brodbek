#!/usr/bin/bash

# assign variables to arguments from the job config
CLUSTER_ID=$1
PROC_ID=$2
SAVE_DIR_0=$3
WHICH_PROCESS=$4

# assign variables
ID=${CLUSTER_ID}_${PROC_ID}
NUM_EVENTS=1000
OUTPUT_FILENAME=${WHICH_PROCESS}_${ID}.root
WORK_DIR=/work/gbrodbek/FCC_fullsim/FullSim_TauID/files_for_generation_chain
SAVE_DIR=${SAVE_DIR_0}/${WHICH_PROCESS}
TEMP_FILES=${SAVE_DIR}/temporaryFiles

# go to working directory
cd ${WORK_DIR}

# source the key4hep stack
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh -r 2024-12-22

# generate events in pythia
k4run pythia.py -n $NUM_EVENTS --Dumper.Filename ${TEMP_FILES}/out_temp_${ID}.hepmc --Pythia8.PythiaInterface.pythiacard Zcards/Zcard_${WHICH_PROCESS}.cmd

# run cld detector full simulation
ddsim --compactFile CLD_o2_v06/CLD_o2_v06.xml --outputFile ${TEMP_FILES}/out_sim_edm4hep_temp_${ID}.root --steeringFile cld_steer.py --inputFiles ${TEMP_FILES}/out_temp_${ID}.hepmc --numberOfEvents $NUM_EVENTS --random.seed ${PROC_ID}+1

# run reconstruction
k4run CLDReconstruction.py -n $NUM_EVENTS  --inputFile ${TEMP_FILES}/out_sim_edm4hep_temp_${ID}.root --outputBasename ${TEMP_FILES}/out_reco_edm4hep_temp_${ID}

# produce flat tree
python pftree_maker_from_dolores/make_pftree_clic_bindings_tautau.py ${TEMP_FILES}/out_reco_edm4hep_temp_${ID}_edm4hep.root ${SAVE_DIR}/outputFiles/${OUTPUT_FILENAME} False False 0