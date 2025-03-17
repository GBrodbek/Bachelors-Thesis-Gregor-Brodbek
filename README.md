# Bachelor's Thesis Gregor Brodbek

This repository contains all scripts and files of the Bachelor's Thesis "Tau Reconstruction at FCC-ee using Machine Learning based on Full Detector Simulation" by Gregor Brodbek.

Everything inside the directory modelTrain/PID_GNN is adapted from [Dolores Garcia's work](https://github.com/doloresgarcia/PID_GNN).


## Generation of Full Detector Simulation Samples

The event generation chain looks like this:

1) Source the key4hep nightlie build. One of the functions in the treemaker wasn't working with the newer versions, so I was using the version 2024-09-21.
2) Monte Carlo simulation with Pythia8
3) Detector simulation with geant4
4) Pandora reconstruction
5) Treemaker by Dolores

I wrote a [script](./files_for_generation_chain/condorSubmission/submitFullsim.sh), that automatically submits the whole simulation process to HTCondor at ETP. Different Pythia cards for different processes can be found [here](./files_for_generation_chain/Zcards). Also Xunwu made a [repository](https://github.com/zuoxunwu/FullSim_TauID), that explains the whole generation process in more detail.
