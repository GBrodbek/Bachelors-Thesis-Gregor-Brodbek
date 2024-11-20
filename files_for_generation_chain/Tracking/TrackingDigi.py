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


VXDBarrelDigitiser = MarlinProcessorWrapper("VXDBarrelDigitiser")
VXDBarrelDigitiser.OutputLevel = WARNING
VXDBarrelDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDBarrelDigitiser.Parameters = {
                                 "IsStrip": ["false"],
                                 "ResolutionU": ["0.003", "0.003", "0.003", "0.003", "0.003", "0.003"],
                                 "ResolutionV": ["0.003", "0.003", "0.003", "0.003", "0.003", "0.003"],
                                 "SimTrackHitCollectionName": ["VertexBarrelCollection"],
                                 "SimTrkHitRelCollection": ["VXDTrackerHitRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TrackerHitCollectionName": ["VXDTrackerHits"]
                                 }

VXDEndcapDigitiser = MarlinProcessorWrapper("VXDEndcapDigitiser")
VXDEndcapDigitiser.OutputLevel = WARNING
VXDEndcapDigitiser.ProcessorType = "DDPlanarDigiProcessor"
VXDEndcapDigitiser.Parameters = {
                                 "IsStrip": ["false"],
                                 "ResolutionU": ["0.003", "0.003", "0.003", "0.003", "0.003", "0.003"],
                                 "ResolutionV": ["0.003", "0.003", "0.003", "0.003", "0.003", "0.003"],
                                 "SimTrackHitCollectionName": ["VertexEndcapCollection"],
                                 "SimTrkHitRelCollection": ["VXDEndcapTrackerHitRelations"],
                                 "SubDetectorName": ["Vertex"],
                                 "TrackerHitCollectionName": ["VXDEndcapTrackerHits"]
                                 }

InnerPlanarDigiProcessor = MarlinProcessorWrapper("InnerPlanarDigiProcessor")
InnerPlanarDigiProcessor.OutputLevel = WARNING
InnerPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerPlanarDigiProcessor.Parameters = {
                                       "IsStrip": ["false"],
                                       "ResolutionU": ["0.007"],
                                       "ResolutionV": ["0.09"],
                                       "SimTrackHitCollectionName": ["InnerTrackerBarrelCollection"],
                                       "SimTrkHitRelCollection": ["InnerTrackerBarrelHitsRelations"],
                                       "SubDetectorName": ["InnerTrackers"],
                                       "TrackerHitCollectionName": ["ITrackerHits"]
                                       }

InnerEndcapPlanarDigiProcessor = MarlinProcessorWrapper("InnerEndcapPlanarDigiProcessor")
InnerEndcapPlanarDigiProcessor.OutputLevel = WARNING
InnerEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
InnerEndcapPlanarDigiProcessor.Parameters = {
                                             "IsStrip": ["false"],
                                             "ResolutionU": ["0.005", "0.007", "0.007", "0.007", "0.007", "0.007", "0.007"],
                                             "ResolutionV": ["0.005", "0.09", "0.09", "0.09", "0.09", "0.09", "0.09"],
                                             "SimTrackHitCollectionName": ["InnerTrackerEndcapCollection"],
                                             "SimTrkHitRelCollection": ["InnerTrackerEndcapHitsRelations"],
                                             "SubDetectorName": ["InnerTrackers"],
                                             "TrackerHitCollectionName": ["ITrackerEndcapHits"]
                                             }

OuterPlanarDigiProcessor = MarlinProcessorWrapper("OuterPlanarDigiProcessor")
OuterPlanarDigiProcessor.OutputLevel = WARNING
OuterPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterPlanarDigiProcessor.Parameters = {
                                       "IsStrip": ["false"],
                                       "ResolutionU": ["0.007", "0.007", "0.007"],
                                       "ResolutionV": ["0.09", "0.09", "0.09"],
                                       "SimTrackHitCollectionName": ["OuterTrackerBarrelCollection"],
                                       "SimTrkHitRelCollection": ["OuterTrackerBarrelHitsRelations"],
                                       "SubDetectorName": ["OuterTrackers"],
                                       "TrackerHitCollectionName": ["OTrackerHits"]
                                       }

OuterEndcapPlanarDigiProcessor = MarlinProcessorWrapper("OuterEndcapPlanarDigiProcessor")
OuterEndcapPlanarDigiProcessor.OutputLevel = WARNING
OuterEndcapPlanarDigiProcessor.ProcessorType = "DDPlanarDigiProcessor"
OuterEndcapPlanarDigiProcessor.Parameters = {
                                             "IsStrip": ["false"],
                                             "ResolutionU": ["0.007", "0.007", "0.007", "0.007", "0.007"],
                                             "ResolutionV": ["0.09", "0.09", "0.09", "0.09", "0.09"],
                                             "SimTrackHitCollectionName": ["OuterTrackerEndcapCollection"],
                                             "SimTrkHitRelCollection": ["OuterTrackerEndcapHitsRelations"],
                                             "SubDetectorName": ["OuterTrackers"],
                                             "TrackerHitCollectionName": ["OTrackerEndcapHits"]
                                             }

TrackingDigiSequence = [
    VXDBarrelDigitiser,
    VXDEndcapDigitiser,
    InnerPlanarDigiProcessor,
    InnerEndcapPlanarDigiProcessor,
    OuterPlanarDigiProcessor,
    OuterEndcapPlanarDigiProcessor,
]
