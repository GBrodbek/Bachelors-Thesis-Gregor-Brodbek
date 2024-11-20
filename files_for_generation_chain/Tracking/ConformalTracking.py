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


# geoservice comes from the `global_vars` of the SequenceLoader
if any(small_vtx in geoservice.detectors[0] for small_vtx in ["_o2_", "_o3_", "_o4_"]):
    CT_MAX_DIST = "0.05;"  # semi-colon is important!
elif "_o1_" in  geoservice.detectors[0]:
    CT_MAX_DIST = "0.03;"  # semi-colon is important!
else:
    raise RuntimeError("Unknown detector model to chose CT_MAX_DISTANCE")

MyConformalTracking = MarlinProcessorWrapper("MyConformalTracking")
MyConformalTracking.OutputLevel = WARNING
MyConformalTracking.ProcessorType = "ConformalTrackingV2"
MyConformalTracking.Parameters = {
                                  "DebugHits": ["DebugHits"],
                                  "DebugPlots": ["false"],
                                  "DebugTiming": ["false"],
                                  "MCParticleCollectionName": ["MCParticle"],
                                  "MaxHitInvertedFit": ["0"],
                                  "MinClustersOnTrackAfterFit": ["3"],
                                  "RelationsNames": ["VXDTrackerHitRelations", "VXDEndcapTrackerHitRelations", "InnerTrackerBarrelHitsRelations", "OuterTrackerBarrelHitsRelations", "InnerTrackerEndcapHitsRelations", "OuterTrackerEndcapHitsRelations"],
                                  "RetryTooManyTracks": ["false"],
                                  "SiTrackCollectionName": ["SiTracksCT"],
                                  "SortTreeResults": ["true"],
                                  "Steps":
                                  [
                                      "[VXDBarrel]",
                                      "@Collections", ":", "VXDTrackerHits",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.01;", "MaxCellAngleRZ", ":", "0.01;", "Chi2Cut", ":", "100;", "MinClustersOnTrack", ":", "4;", "MaxDistance", ":", CT_MAX_DIST, "SlopeZRange:", "10.0;", "HighPTCut:", "10.0;",
                                      "@Flags", ":", "HighPTFit,", "VertexToTracker",
                                      "@Functions", ":", "CombineCollections,", "BuildNewTracks",
                                      "[VXDEncap]",
                                      "@Collections", ":", "VXDEndcapTrackerHits",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.01;", "MaxCellAngleRZ", ":", "0.01;", "Chi2Cut", ":", "100;", "MinClustersOnTrack", ":", "4;", "MaxDistance", ":", CT_MAX_DIST, "SlopeZRange:", "10.0;", "HighPTCut:", "10.0;",
                                      "@Flags", ":", "HighPTFit,", "VertexToTracker",
                                      "@Functions", ":", "CombineCollections,", "ExtendTracks",
                                      "[LowerCellAngle1]",
                                      "@Collections", ":", "VXDTrackerHits,", "VXDEndcapTrackerHits",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.05;", "MaxCellAngleRZ", ":", "0.05;", "Chi2Cut", ":", "100;", "MinClustersOnTrack", ":", "4;", "MaxDistance", ":", CT_MAX_DIST, "SlopeZRange:", "10.0;", "HighPTCut:", "10.0;",
                                      "@Flags", ":", "HighPTFit,", "VertexToTracker,", "RadialSearch",
                                      "@Functions", ":", "CombineCollections,", "BuildNewTracks",
                                      "[LowerCellAngle2]",
                                      "@Collections", ":",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.1;", "MaxCellAngleRZ", ":", "0.1;", "Chi2Cut", ":", "2000;", "MinClustersOnTrack", ":", "4;", "MaxDistance", ":", CT_MAX_DIST, "SlopeZRange:", "10.0;", "HighPTCut:", "10.0;",
                                      "@Flags", ":", "HighPTFit,", "VertexToTracker,", "RadialSearch",
                                      "@Functions", ":", "BuildNewTracks,", "SortTracks",
                                      "[Tracker]",
                                      "@Collections", ":", "ITrackerHits,", "OTrackerHits,", "ITrackerEndcapHits,", "OTrackerEndcapHits",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.1;", "MaxCellAngleRZ", ":", "0.1;", "Chi2Cut", ":", "2000;", "MinClustersOnTrack", ":", "4;", "MaxDistance", ":", CT_MAX_DIST, "SlopeZRange:", "10.0;", "HighPTCut:", "1.0;",
                                      "@Flags", ":", "HighPTFit,", "VertexToTracker,", "RadialSearch",
                                      "@Functions", ":", "CombineCollections,", "ExtendTracks",
                                      "[Displaced]",
                                      "@Collections", ":", "VXDTrackerHits,", "VXDEndcapTrackerHits,", "ITrackerHits,", "OTrackerHits,", "ITrackerEndcapHits,", "OTrackerEndcapHits",
                                      "@Parameters", ":", "MaxCellAngle", ":", "0.1;", "MaxCellAngleRZ", ":", "0.1;", "Chi2Cut", ":", "1000;", "MinClustersOnTrack", ":", "5;", "MaxDistance", ":", "0.015;", "SlopeZRange:", "10.0;", "HighPTCut:", "10.0;",
                                      "@Flags", ":", "OnlyZSchi2cut,", "RadialSearch",
                                      "@Functions", ":", "CombineCollections,", "BuildNewTracks"
                                  ],
                                  "ThetaRange": ["0.05"],
                                  "TooManyTracks": ["100000"],
                                  "TrackerHitCollectionNames": ["VXDTrackerHits", "VXDEndcapTrackerHits", "ITrackerHits", "OTrackerHits", "ITrackerEndcapHits", "OTrackerEndcapHits"],
                                  "trackPurity": ["0.7"]
                                  }

ClonesAndSplitTracksFinder = MarlinProcessorWrapper("ClonesAndSplitTracksFinder")
ClonesAndSplitTracksFinder.OutputLevel = WARNING
ClonesAndSplitTracksFinder.ProcessorType = "ClonesAndSplitTracksFinder"
ClonesAndSplitTracksFinder.Parameters = {
                                         "EnergyLossOn": ["true"],
                                         "InputTrackCollectionName": ["SiTracksCT"],
                                         "MultipleScatteringOn": ["true"],
                                         "OutputTrackCollectionName": ["SiTracks"],
                                         "SmoothOn": ["false"],
                                         "extrapolateForward": ["true"],
                                         "maxSignificancePhi": ["3"],
                                         "maxSignificancePt": ["2"],
                                         "maxSignificanceTheta": ["3"],
                                         "mergeSplitTracks": ["false"],
                                         "minTrackPt": ["1"]
                                         }

ConformalTrackingSequence = [
    MyConformalTracking,
    ClonesAndSplitTracksFinder,
]
