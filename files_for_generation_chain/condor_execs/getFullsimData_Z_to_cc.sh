#!/usr/bin/bash

# assign variables
CLUSTER_ID=$1
PROC_ID=$2
ID=${CLUSTER_ID}_${PROC_ID}
NUM_EVENTS=1000
OUTPUT_FILENAME=Z_to_cc_${ID}.root
WORK_DIR=/work/gbrodbek/FCC_fullsim/FullSim_TauID/files_for_generation_chain
SAVE_DIR=/ceph/gbrodbek/data/background/Z_to_cc
TEMP_FILES=temporaryFiles

cd ${WORK_DIR}
#source the key4hep stack
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

#generate events in pythia
k4run ${WORK_DIR}/pythia.py -n $NUM_EVENTS --Dumper.Filename ${SAVE_DIR}/${TEMP_FILES}/out_temp_${ID}.hepmc --Pythia8.PythiaInterface.pythiacard ${WORK_DIR}/Zcards/Zcard_Z_to_cc.cmd

#run cld detector full simulation
ddsim --compactFile ${WORK_DIR}/CLD_o2_v06/CLD_o2_v06.xml --outputFile ${SAVE_DIR}/${TEMP_FILES}/out_sim_edm4hep_temp_${ID}.root --steeringFile ${WORK_DIR}/cld_steer.py --inputFiles ${SAVE_DIR}/${TEMP_FILES}/out_temp_${ID}.hepmc --numberOfEvents $NUM_EVENTS --random.seed ${PROC_ID}+1

#run reconstruction
k4run ${WORK_DIR}/CLDReconstruction.py -n $NUM_EVENTS  --inputFile ${SAVE_DIR}/${TEMP_FILES}/out_sim_edm4hep_temp_${ID}.root --outputBasename ${SAVE_DIR}/${TEMP_FILES}/out_reco_edm4hep_temp_${ID}

#produce flat tree
python ${WORK_DIR}/pftree_maker_from_dolores/make_pftree_clic_bindings_tautau.py ${SAVE_DIR}/${TEMP_FILES}/out_reco_edm4hep_temp_${ID}_edm4hep.root ${SAVE_DIR}/outputFiles/${OUTPUT_FILENAME} False False 0