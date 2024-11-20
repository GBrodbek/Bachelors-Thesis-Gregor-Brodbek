# FullSim_TauID
This repo accommodates developments of Tau ID based on CLD full simulation, in view of Gregor Brodbek's thesis. \
The workflow is based on [Dolores Garcia's work](https://github.com/doloresgarcia/PID_GNN).  

### Explanation for the basic workflow
The workflow uses full simulation tools for CLD in the [key4hep](https://key4hep.github.io/key4hep-doc/) stack. Necessary commands for the workflow are explained here.\
More details can be found in the [FCC full simulation tutorial](https://hep-fcc.github.io/fcc-tutorials/master/full-detector-simulations/README.html)
#### Setting up environment
Connect to your server that has `/cvmfs` mount and with an OS (Alma9 by default) supported by key4hep.
```
ssh username@portal1.etp.kit.edu
```
Source the nightlie build of `key4hep`
```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```
Go to your work directory and clone this github repo
```
cd /YOUR/WORK/DIR
git clone git@github.com:zuoxunwu/FullSim_TauID.git
```
Everything is set.
 
 

To run the code, the `key4hep` stack needs to be sourced every time you log into the machine
```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```
The directory `files_for_generation_chain` contains all library or configuration needed for running the whole workflow.\
You do not have to source other environment or grab other packages.\
Individual steps of the workflow is explained below. You can run them in the `files_for_generation_chain` directory.
```
cd files_for_generation_chain
```

#### Generate Pythia events
```
k4run pythia.py -n 10 --Dumper.Filename out.hepmc --Pythia8.PythiaInterface.pythiacard Zcard.cmd 
```
The `k4run` command comes from the [k4Gen package](https://github.com/HEP-FCC/k4Gen). It is used to generate pythia samples. It takes the following arguments.
```
k4run [--dry-run] [-v] [-n NUM_EVENTS] [-l] [--gdb] [-h] [config_files ...]
```
- `-n` is the number of events to generate,
- `config_files` is the config file to steer pythia (in our case `pythia.py`). More info on this configuration can be found in the [k4Gen repo](https://github.com/HEP-FCC/k4Gen/blob/main/k4Gen/options/pythia.py)
- `--Pythia8.PythiaInterface.pythiacard` is a option in the `pythia.py` to take a card (`Zcard.cmd`) spefifying pythia settings, which can be found in the [FCC central generator config](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Generator/Pythia8/p8_ee_Ztautau_ecm91.cmd)

#### Run CLD full sim
```
ddsim --compactFile CLD_o2_v06/CLD_o2_v06.xml --outputFile out_sim_edm4hep.root --steeringFile cld_steer.py --inputFiles out.hepmc --numberOfEvents 10 --random.seed 4
```

#### Run reconstruction
```
k4run CLDReconstruction.py -n 10  --inputFile out_sim_edm4hep.root --outputBasename out_reco_edm4hep
```

#### Produce flat tree
```
python pftree_maker_from_dolores/make_pftree_clic_bindings_tautau.py out_reco_edm4hep_edm4hep.root tree2.root False False 0
```
# Studium
# Bachelorarbeit
