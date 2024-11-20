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
from Gaudi.Configuration import WARNING
from Configurables import MarlinProcessorWrapper


MyDDMarlinPandoraParameters = {
                                     "FinalEnergyDensityBin": ["110."],
                                     "MaxClusterEnergyToApplySoftComp": ["200."],
                                     "TrackCollections": ["SiTracks_Refitted"],
                                     "ECalCaloHitCollections": ["ECALBarrel", "ECALEndcap"],
                                     "HCalCaloHitCollections": ["HCALBarrel", "HCALEndcap", "HCALOther"],
                                     "LCalCaloHitCollections": [],
                                     "LHCalCaloHitCollections": [],
                                     "MuonCaloHitCollections": ["MUON"],
                                     "MCParticleCollections": ["MCParticle"],
                                     "RelCaloHitCollections": ["RelationCaloHit", "RelationMuonHit"],
                                     "RelTrackCollections": ["SiTracks_Refitted_Relation"],
                                     "KinkVertexCollections": ["KinkVertices"],
                                     "ProngVertexCollections": ["ProngVertices"],
                                     "SplitVertexCollections": ["SplitVertices"],
                                     "V0VertexCollections": ["V0Vertices"],
                                     "ClusterCollectionName": ["PandoraClusters"],
                                     "PFOCollectionName": ["PandoraPFOs"],
                                     "UseOldTrackStateCalculation": ["0"],
                                     "NEventsToSkip": ["0"],
                                     "CreateGaps": ["false"],
                                     "MinBarrelTrackerHitFractionOfExpected": ["0"],
                                     "MinFtdHitsForBarrelTrackerHitFraction": ["0"],
                                     "MinFtdTrackHits": ["0"],
                                     "MinMomentumForTrackHitChecks": ["0"],
                                     "MinTpcHitFractionOfExpected": ["0"],
                                     "MinTrackECalDistanceFromIp": ["0"],
                                     "MinTrackHits": ["0"],
                                     "ReachesECalBarrelTrackerOuterDistance": ["-100"],
                                     "ReachesECalBarrelTrackerZMaxDistance": ["-50"],
                                     "ReachesECalFtdZMaxDistance": ["1"],
                                     "ReachesECalMinFtdLayer": ["0"],
                                     "ReachesECalNBarrelTrackerHits": ["0"],
                                     "ReachesECalNFtdHits": ["0"],
                                     "UnmatchedVertexTrackMaxEnergy": ["5"],
                                     "UseNonVertexTracks": ["1"],
                                     "UseUnmatchedNonVertexTracks": ["0"],
                                     "UseUnmatchedVertexTracks": ["1"],
                                     "Z0TrackCut": ["200"],
                                     "Z0UnmatchedVertexTrackCut": ["5"],
                                     "ZCutForNonVertexTracks": ["250"],
                                     "MaxTrackHits": ["5000"],
                                     "MaxTrackSigmaPOverP": ["0.15"],
                                     "CurvatureToMomentumFactor": ["0.00015"],
                                     "D0TrackCut": ["200"],
                                     "D0UnmatchedVertexTrackCut": ["5"],
                                     "StartVertexAlgorithmName": ["PandoraPFANew"],
                                     "StartVertexCollectionName": ["PandoraStartVertices"],
                                     "YokeBarrelNormalVector": ["0", "0", "1"],
                                     "HCalBarrelNormalVector": ["0", "0", "1"],
                                     "ECalBarrelNormalVector": ["0", "0", "1"],
                                     "MuonBarrelBField": ["-1.0"],
                                     "MuonEndCapBField": ["0.01"],
                                     "EMConstantTerm": ["0.01"],
                                     "EMStochasticTerm": ["0.17"],
                                     "HadConstantTerm": ["0.03"],
                                     "HadStochasticTerm": ["0.6"],
                                     "InputEnergyCorrectionPoints": [],
                                     "LayersFromEdgeMaxRearDistance": ["250"],
                                     "NOuterSamplingLayers": ["3"],
                                     "TrackStateTolerance": ["0"],
                                     "MaxBarrelTrackerInnerRDistance": ["200"],
                                     "MinCleanCorrectedHitEnergy": ["0.1"],
                                     "MinCleanHitEnergy": ["0.5"],
                                     "MinCleanHitEnergyFraction": ["0.01"],
                                     "MuonHitEnergy": ["0.5"],
                                     "ShouldFormTrackRelationships": ["1"],
                                     "TrackCreatorName": ["DDTrackCreatorCLIC"],
                                     "TrackSystemName": ["DDKalTest"],
                                     "OutputEnergyCorrectionPoints": [],
                                     "UseEcalScLayers": ["0"],
                                     "ECalScMipThreshold": ["0"],
                                     "ECalScToEMGeVCalibration": ["1"],
                                     "ECalScToHadGeVCalibrationBarrel": ["1"],
                                     "ECalScToHadGeVCalibrationEndCap": ["1"],
                                     "ECalScToMipCalibration": ["1"],
                                     "ECalSiMipThreshold": ["0"],
                                     "ECalSiToEMGeVCalibration": ["1"],
                                     "ECalSiToHadGeVCalibrationBarrel": ["1"],
                                     "ECalSiToHadGeVCalibrationEndCap": ["1"],
                                     "ECalSiToMipCalibration": ["1"],
                                     "StripSplittingOn": ["0"],
}

MyDDMarlinPandora = {}

MyDDMarlinPandora["10ns"] = MarlinProcessorWrapper("MyDDMarlinPandora_10ns")
MyDDMarlinPandora["10ns"].OutputLevel = WARNING
MyDDMarlinPandora["10ns"].ProcessorType = "DDPandoraPFANewProcessor"
MyDDMarlinPandora["10ns"].Parameters = MyDDMarlinPandoraParameters.copy()
MyDDMarlinPandora["10ns"].Parameters |= {
                                     "PandoraSettingsXmlFile": ["PandoraSettingsCLD/PandoraSettingsDefault.xml"],
                                     "SoftwareCompensationWeights": ["2.40821", "-0.0515852", "0.000711414", "-0.0254891", "-0.0121505", "-1.63084e-05", "0.062149", "0.0690735", "-0.223064"],
                                     "ECalToMipCalibration": ["175.439"],
                                     "HCalToMipCalibration": ["45.6621"],
                                     "ECalMipThreshold": ["0.5"],
                                     "HCalMipThreshold": ["0.3"],
                                     "ECalToEMGeVCalibration": ["1.01776966108"],
                                     "HCalToEMGeVCalibration": ["1.01776966108"],
                                     "ECalToHadGeVCalibrationBarrel": ["1.11490774181"],
                                     "ECalToHadGeVCalibrationEndCap": ["1.11490774181"],
                                     "HCalToHadGeVCalibration": ["1.00565042407"],
                                     "MuonToMipCalibration": ["20703.9"],
                                     "DigitalMuonHits": ["0"],
                                     "MaxHCalHitHadronicEnergy": ["10000000."],
                                     }

MyDDMarlinPandora["400ns"] = MarlinProcessorWrapper("MyDDMarlinPandora_400ns")
MyDDMarlinPandora["400ns"].OutputLevel = WARNING
MyDDMarlinPandora["400ns"].ProcessorType = "DDPandoraPFANewProcessor"
MyDDMarlinPandora["400ns"].Parameters = MyDDMarlinPandoraParameters.copy()
MyDDMarlinPandora["400ns"].Parameters |= {
                                      "PandoraSettingsXmlFile": ["PandoraSettingsCLD/PandoraSettingsDefault_400nsCalTimeWindow.xml"],
                                      "SoftwareCompensationWeights": ["2.43375", "-0.0430951", "0.000244914", "-0.145478", "-0.00044577", "-8.37222e-05", "0.237484", "0.243491", "-0.0713701"],
                                      "ECalToMipCalibration": ["175.439"],
                                      "HCalToMipCalibration": ["49.7512"],
                                      "ECalMipThreshold": ["0.5"],
                                      "HCalMipThreshold": ["0.3"],
                                      "ECalToEMGeVCalibration": ["1.02513816926"],
                                      "HCalToEMGeVCalibration": ["1.02513816926"],
                                      "ECalToHadGeVCalibrationBarrel": ["1.07276660331"],
                                      "ECalToHadGeVCalibrationEndCap": ["1.07276660331"],
                                      "HCalToHadGeVCalibration": ["1.01147686143"],
                                      "MuonToMipCalibration": ["20703.9"],
                                      "DigitalMuonHits": ["0"],
                                      "MaxHCalHitHadronicEnergy": ["10000000."],
                                      }

PandoraSequence = [
    MyDDMarlinPandora[CONFIG["CalorimeterIntegrationTimeWindow"]]
]
