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


MyRecoMCTruthLinker = MarlinProcessorWrapper("MyRecoMCTruthLinker")
MyRecoMCTruthLinker.OutputLevel = WARNING
MyRecoMCTruthLinker.ProcessorType = "RecoMCTruthLinker"
MyRecoMCTruthLinker.Parameters = {
                                  "BremsstrahlungEnergyCut": ["1"],
                                  "CalohitMCTruthLinkName": ["CalohitMCTruthLink"],
                                  "ClusterCollection": ["PandoraClusters"],
                                  "ClusterMCTruthLinkName": ["ClusterMCTruthLink"],
                                  "FullRecoRelation": ["true"],
                                  "InvertedNonDestructiveInteractionLogic": ["false"],
                                  "KeepDaughtersPDG": ["22", "111", "310", "13", "211", "321", "3120"],
                                  "MCParticleCollection": ["MCPhysicsParticles"],
                                  "MCParticlesSkimmedName": ["MCParticlesSkimmed"],
                                  "MCTruthClusterLinkName": ["MCTruthClusterLink"],
                                  "MCTruthRecoLinkName": ["MCTruthRecoLink"],
                                  "MCTruthTrackLinkName": ["MCTruthSiTracksLink"],
                                  "RecoMCTruthLinkName": ["RecoMCTruthLink"],
                                  "RecoParticleCollection": ["PandoraPFOs"],
                                  "SaveBremsstrahlungPhotons": ["true"],
                                  "SimCaloHitCollections": ["ECalBarrelCollection", "ECalEndcapCollection", "HCalBarrelCollection", "HCalEndcapCollection", "HCalRingCollection", "YokeBarrelCollection", "YokeEndcapCollection", "LumiCalCollection"],
                                  "SimCalorimeterHitRelationNames": ["RelationCaloHit", "RelationMuonHit"],
                                  "SimTrackerHitCollections": ["VertexBarrelCollection", "VertexEndcapCollection", "InnerTrackerBarrelCollection", "OuterTrackerBarrelCollection", "InnerTrackerEndcapCollection", "OuterTrackerEndcapCollection"],
                                  "TrackCollection": ["SiTracks_Refitted"],
                                  "TrackMCTruthLinkName": ["SiTracksMCTruthLink"],
                                  "TrackerHitsRelInputCollections": ["VXDTrackerHitRelations", "VXDEndcapTrackerHitRelations", "InnerTrackerBarrelHitsRelations", "OuterTrackerBarrelHitsRelations", "InnerTrackerEndcapHitsRelations", "OuterTrackerEndcapHitsRelations"],
                                  "UseTrackerHitRelations": ["true"],
                                  "UsingParticleGun": ["false"],
                                  "daughtersECutMeV": ["10"]
                                  }

RecoMCTruthLinkSequence = [
    MyRecoMCTruthLinker,
]
