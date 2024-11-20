#
# Copyright (c) 2014-2024 Key4hep-Project.
#
# This file is part of Key4hep.
# See https://key4hep.github.io/key4hep-doc/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from Gaudi.Configuration import INFO, WARNING, DEBUG

from Configurables import k4DataSvc, MarlinProcessorWrapper
from k4MarlinWrapper.inputReader import create_reader, attach_edm4hep2lcio_conversion
from k4FWCore.parseArgs import parser
from py_utils import SequenceLoader

import ROOT
ROOT.gROOT.SetBatch(True)


parser.add_argument("--inputFiles", action="extend", nargs="+", metavar=("file1", "file2"), help="One or multiple input files")
parser.add_argument("--outputBasename", help="Basename of the output file(s)", default="output")
parser.add_argument("--trackingOnly", action="store_true", help="Run only track reconstruction", default=False)
parser.add_argument("--enableLCFIJet", action="store_true", help="Enable LCFIPlus jet clustering parts", default=False)
reco_args = parser.parse_known_args()[0]

algList = []
svcList = []

evtsvc = k4DataSvc("EventDataSvc")
svcList.append(evtsvc)

CONFIG = {
             "CalorimeterIntegrationTimeWindow": "10ns",
             "CalorimeterIntegrationTimeWindowChoices": ["10ns", "400ns"],
             "Overlay": "False",
             "OverlayChoices": ["False", "91GeV", "365GeV"],
             "Tracking": "Conformal",
             "TrackingChoices": ["Truth", "Conformal"],
             "VertexUnconstrained": "OFF",
             "VertexUnconstrainedChoices": ["ON", "OFF"],
             "OutputMode": "EDM4Hep",
             "OutputModeChoices": ["LCIO", "EDM4hep"] #, "both"] FIXME: both is not implemented yet
}

from Configurables import GeoSvc, TrackingCellIDEncodingSvc
geoservice = GeoSvc("GeoSvc")
geoservice.detectors = [os.environ["K4GEO"]+"/FCCee/CLD/compact/CLD_o2_v06/CLD_o2_v06.xml"]
geoservice.OutputLevel = INFO
geoservice.EnableGeant4Geo = False
svcList.append(geoservice)

cellIDSvc = TrackingCellIDEncodingSvc("CellIDSvc")
cellIDSvc.EncodingStringParameterName = "GlobalTrackerReadoutID"
cellIDSvc.GeoSvcName = geoservice.name()
cellIDSvc.OutputLevel = INFO
svcList.append(cellIDSvc)

if len(geoservice.detectors) > 1:
    # we are making assumptions for reconstruction parameters based on the detector option, so we limit the possibilities
    raise RuntimeError("Too many XML files for the detector path, please only specify the main file!")

sequenceLoader = SequenceLoader(
    algList,
    # global_vars can be used in sequence-loaded modules without explicit import
    global_vars={"CONFIG": CONFIG, "geoservice": geoservice, "reco_args": reco_args},
)

if reco_args.inputFiles:
    read = create_reader(reco_args.inputFiles, evtsvc)
    read.OutputLevel = INFO
    algList.append(read)
else:
    read = None

MyAIDAProcessor = MarlinProcessorWrapper("MyAIDAProcessor")
MyAIDAProcessor.OutputLevel = WARNING
MyAIDAProcessor.ProcessorType = "AIDAProcessor"
MyAIDAProcessor.Parameters = {
                              "Compress": ["1"],
                              "FileName": [f"{reco_args.outputBasename}_aida"],
                              "FileType": ["root"]
                              }

EventNumber = MarlinProcessorWrapper("EventNumber")
EventNumber.OutputLevel = WARNING
EventNumber.ProcessorType = "Statusmonitor"
EventNumber.Parameters = {
                          "HowOften": ["1"]
                          }

# TODO: put this somewhere else, needs to be in front of the output for now :(
# setup AIDA histogramming and add eventual background overlay
algList.append(MyAIDAProcessor)
sequenceLoader.load("Overlay/Overlay")
# tracker hit digitisation
sequenceLoader.load("Tracking/TrackingDigi")

# tracking
if CONFIG["Tracking"] == "Truth":
    sequenceLoader.load("Tracking/TruthTracking")
elif CONFIG["Tracking"] == "Conformal":
    sequenceLoader.load("Tracking/ConformalTracking")

sequenceLoader.load("Tracking/Refit")

# calorimeter digitization and pandora
if not reco_args.trackingOnly:
    sequenceLoader.load("CaloDigi/CaloDigi")
    sequenceLoader.load("CaloDigi/MuonDigi")
    sequenceLoader.load("ParticleFlow/Pandora")
    sequenceLoader.load("CaloDigi/LumiCal")
# monitoring and Reco to MCTruth linking
sequenceLoader.load("HighLevelReco/RecoMCTruthLink")
sequenceLoader.load("Diagnostics/Tracking")
# pfo selector (might need re-optimisation)
if not reco_args.trackingOnly:
    sequenceLoader.load("HighLevelReco/PFOSelector")
    sequenceLoader.load("HighLevelReco/JetClusteringOrRenaming")
    sequenceLoader.load("HighLevelReco/JetAndVertex")
# event number processor, down here to attach the conversion back to edm4hep to it
algList.append(EventNumber)

if CONFIG["OutputMode"] == "LCIO":
    Output_REC = MarlinProcessorWrapper("Output_REC")
    Output_REC.OutputLevel = WARNING
    Output_REC.ProcessorType = "LCIOOutputProcessor"
    Output_REC.Parameters = {
                             "DropCollectionNames": [],
                             "DropCollectionTypes": [],
                             "FullSubsetCollections": ["EfficientMCParticles", "InefficientMCParticles"],
                             "KeepCollectionNames": [],
                             "LCIOOutputFile": [f"{reco_args.outputBasename}_REC.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }

    Output_DST = MarlinProcessorWrapper("Output_DST")
    Output_DST.OutputLevel = WARNING
    Output_DST.ProcessorType = "LCIOOutputProcessor"
    Output_DST.Parameters = {
                             "DropCollectionNames": [],
                             "DropCollectionTypes": ["MCParticle", "LCRelation", "SimCalorimeterHit", "CalorimeterHit", "SimTrackerHit", "TrackerHit", "TrackerHitPlane", "Track", "ReconstructedParticle", "LCFloatVec"],
                             "FullSubsetCollections": ["EfficientMCParticles", "InefficientMCParticles", "MCPhysicsParticles"],
                             "KeepCollectionNames": ["MCParticlesSkimmed", "MCPhysicsParticles", "RecoMCTruthLink", "SiTracks", "SiTracks_Refitted", "PandoraClusters", "PandoraPFOs", "SelectedPandoraPFOs", "LooseSelectedPandoraPFOs", "TightSelectedPandoraPFOs", "RefinedVertexJets", "RefinedVertexJets_rel", "RefinedVertexJets_vtx", "RefinedVertexJets_vtx_RP", "BuildUpVertices", "BuildUpVertices_res", "BuildUpVertices_RP", "BuildUpVertices_res_RP", "BuildUpVertices_V0", "BuildUpVertices_V0_res", "BuildUpVertices_V0_RP", "BuildUpVertices_V0_res_RP", "PrimaryVertices", "PrimaryVertices_res", "PrimaryVertices_RP", "PrimaryVertices_res_RP", "RefinedVertices", "RefinedVertices_RP"],
                             "LCIOOutputFile": [f"{reco_args.outputBasename}_DST.slcio"],
                             "LCIOWriteMode": ["WRITE_NEW"]
                             }
    algList.append(Output_REC)
    algList.append(Output_DST)

if CONFIG["OutputMode"] == "EDM4Hep":
    from Configurables import Lcio2EDM4hepTool
    lcioConvTool = Lcio2EDM4hepTool("lcio2EDM4hep")
    lcioConvTool.convertAll = True
    lcioConvTool.collNameMapping = {
        "MCParticle": "MCParticles"
    }
    lcioConvTool.OutputLevel = DEBUG
# attach to the last non output processor
    EventNumber.Lcio2EDM4hepTool = lcioConvTool

    from Configurables import PodioOutput
    out = PodioOutput("PodioOutput", filename = f"{reco_args.outputBasename}_edm4hep.root")
    out.outputCommands = ["keep *"]
    algList.append(out)

# We need to convert the inputs in case we have EDM4hep input
attach_edm4hep2lcio_conversion(algList, read)

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = algList,
                EvtSel = 'NONE',
                EvtMax = 3, # Overridden by the --num-events switch to k4run
                ExtSvc = svcList,
                OutputLevel=WARNING
              )
