#!/usr/bin/bash
CLUSTER_ID=$1
PROC_ID=$2
ID=${CLUSTER_ID}_${PROC_ID}
OUTPUT_FILENAME=background_${ID}.root
WORK_DIR=/work/gbrodbek/FCC_fullsim/FullSim_TauID/files_for_generation_chain
SAVE_DIR=/ceph/gbrodbek/data/background
TEMP_FILES=temporaryFiles
FILENAME=out_reco_edm4hep_temp_1151259_${PROC_ID}_edm4hep.root    # name of the file to be rerun

cd ${WORK_DIR}
#source the key4hep stack
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh


python ${WORK_DIR}/pftree_maker_from_dolores/make_pftree_clic_bindings_tautau.py ${SAVE_DIR}/${TEMP_FILES}/${FILENAME} ${SAVE_DIR}/outputFiles_correctLabels/${OUTPUT_FILENAME} False False 0