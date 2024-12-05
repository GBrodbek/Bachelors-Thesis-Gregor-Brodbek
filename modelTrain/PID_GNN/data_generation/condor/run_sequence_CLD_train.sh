#!/bin/bash

HOMEDIR=${1}
GUNCARD=${2}
NEV=${3}
SEED=${4}
OUTPUTDIR=${5}
DIR=${6}
IDX=${7}

SAMPLE="Zcard" #main card

mkdir ${DIR}
mkdir ${DIR}/${SEED}
cd ${DIR}/${SEED}


if [[ "${SAMPLE}" == "gun" ]] 
then 
cp -r ${HOMEDIR}/gun/gun.cpp .
cp -r ${HOMEDIR}/gun/CMakeLists.txt . 
fi 

if [[ "${SAMPLE}" == "Zcard" ]]
then 
      cp ${HOMEDIR}/Pythia_generation/${SAMPLE}.cmd card.cmd
      echo "Random:seed=${SEED}" >> card.cmd
      cat card.cmd
      cp ${HOMEDIR}/Pythia_generation/pythia.py ./
fi

##

cp -r /afs/cern.ch/work/m/mgarciam/private/CLDConfig_2207/CLDConfig/* .
cp -r ${HOMEDIR}/condor/make_pftree_clic_bindings_tautau.py .
cp -r ${HOMEDIR}/condor/tree_tools_tautau.py .
cp -r ${HOMEDIR}/gun/${GUNCARD} .

# Load key4hep 
wrapperfunction() {
#     source /cvmfs/sw.hsf.org/key4hep/setup.sh
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh 
}
wrapperfunction

if [[ "${SAMPLE}" == "gun" ]] 
then 
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install -j 8
cd ..
./build/gun ${GUNCARD} 
fi 


if [[ "${SAMPLE}" == "Zcard" ]]
then
      k4run pythia.py -n $NEV --Dumper.Filename out.hepmc --Pythia8.PythiaInterface.pythiacard card.cmd
fi


# Run simulation 
ddsim --compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v06/CLD_o2_v06.xml --outputFile out_sim_edm4hep.root --steeringFile cld_steer.py --inputFiles out.hepmc --numberOfEvents ${NEV} --random.seed ${SEED}

# Run reco 
k4run CLDReconstruction.py -n ${NEV}  --inputFile out_sim_edm4hep.root --outputBasename out_reco_edm4hep

# Create Tree 
python make_pftree_clic_bindings_tautau.py out_reco_edm4hep_edm4hep.root tree2.root False False ${IDX}

mkdir -p ${OUTPUTDIR}
python /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py tree2.root ${OUTPUTDIR}/pf_tree_${SEED}.root

