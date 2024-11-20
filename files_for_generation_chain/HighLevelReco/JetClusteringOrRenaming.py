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


RenameCollection = MarlinProcessorWrapper("RenameCollection")
RenameCollection.OutputLevel = WARNING
RenameCollection.ProcessorType = "MergeCollections"
RenameCollection.Parameters = {
                               "CollectionParameterIndex": ["0"],
                               "InputCollectionIDs": [],
                               "InputCollections": ["PandoraPFOs"],
                               "OutputCollection": ["PFOsFromJets"]
                               }

MyFastJetProcessor = MarlinProcessorWrapper("MyFastJetProcessor")
MyFastJetProcessor.OutputLevel = WARNING
MyFastJetProcessor.ProcessorType = "FastJetProcessor"
MyFastJetProcessor.Parameters = {
                                 "algorithm": ["ValenciaPlugin", "1.2", "1.0", "0.7"],
                                 "clusteringMode": ["ExclusiveNJets", "2"],
                                 "jetOut": ["JetsAfterGamGamRemoval"],
                                 "recParticleIn": ["TightSelectedPandoraPFOs"],
                                 "recParticleOut": ["PFOsFromJets"],
                                 "recombinationScheme": ["E_scheme"],
                                 "storeParticlesInJets": ["true"]
                                 }

JetClusteringOrRenamingSequence = []
if CONFIG["Overlay"] == "False":
    JetClusteringOrRenamingSequence.append(RenameCollection)
else:
    JetClusteringOrRenamingSequence.append(MyFastJetProcessor)
