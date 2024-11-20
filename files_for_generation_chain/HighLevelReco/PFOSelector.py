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


MyCLICPfoSelectorDefault = MarlinProcessorWrapper("MyCLICPfoSelectorDefault")
MyCLICPfoSelectorDefault.OutputLevel = WARNING
MyCLICPfoSelectorDefault.ProcessorType = "CLICPfoSelector"
MyCLICPfoSelectorDefault.Parameters = {
                                       "ChargedPfoLooseTimingCut": ["3"],
                                       "ChargedPfoNegativeLooseTimingCut": ["-1"],
                                       "ChargedPfoNegativeTightTimingCut": ["-0.5"],
                                       "ChargedPfoPtCut": ["0"],
                                       "ChargedPfoPtCutForLooseTiming": ["4"],
                                       "ChargedPfoTightTimingCut": ["1.5"],
                                       "CheckKaonCorrection": ["0"],
                                       "CheckProtonCorrection": ["0"],
                                       "ClusterLessPfoTrackTimeCut": ["10"],
                                       "CorrectHitTimesForTimeOfFlight": ["0"],
                                       "DisplayRejectedPfos": ["1"],
                                       "DisplaySelectedPfos": ["1"],
                                       "FarForwardCosTheta": ["0.975"],
                                       "ForwardCosThetaForHighEnergyNeutralHadrons": ["0.95"],
                                       "ForwardHighEnergyNeutralHadronsEnergy": ["10"],
                                       "HCalBarrelLooseTimingCut": ["20"],
                                       "HCalBarrelTightTimingCut": ["10"],
                                       "HCalEndCapTimingFactor": ["1"],
                                       "InputPfoCollection": ["PandoraPFOs"],
                                       "KeepKShorts": ["1"],
                                       "MaxMomentumForClusterLessPfos": ["2"],
                                       "MinECalHitsForTiming": ["5"],
                                       "MinHCalEndCapHitsForTiming": ["5"],
                                       "MinMomentumForClusterLessPfos": ["0.5"],
                                       "MinPtForClusterLessPfos": ["0.5"],
                                       "MinimumEnergyForNeutronTiming": ["1"],
                                       "Monitoring": ["0"],
                                       "MonitoringPfoEnergyToDisplay": ["1"],
                                       "NeutralFarForwardLooseTimingCut": ["2"],
                                       "NeutralFarForwardTightTimingCut": ["1"],
                                       "NeutralHadronBarrelPtCutForLooseTiming": ["3.5"],
                                       "NeutralHadronLooseTimingCut": ["2.5"],
                                       "NeutralHadronPtCut": ["0"],
                                       "NeutralHadronPtCutForLooseTiming": ["8"],
                                       "NeutralHadronTightTimingCut": ["1.5"],
                                       "PhotonFarForwardLooseTimingCut": ["2"],
                                       "PhotonFarForwardTightTimingCut": ["1"],
                                       "PhotonLooseTimingCut": ["2"],
                                       "PhotonPtCut": ["0"],
                                       "PhotonPtCutForLooseTiming": ["4"],
                                       "PhotonTightTimingCut": ["1"],
                                       "PtCutForTightTiming": ["0.75"],
                                       "SelectedPfoCollection": ["SelectedPandoraPFOs"],
                                       "UseClusterLessPfos": ["1"],
                                       "UseNeutronTiming": ["0"]
                                       }

MyCLICPfoSelectorLoose = MarlinProcessorWrapper("MyCLICPfoSelectorLoose")
MyCLICPfoSelectorLoose.OutputLevel = WARNING
MyCLICPfoSelectorLoose.ProcessorType = "CLICPfoSelector"
MyCLICPfoSelectorLoose.Parameters = {
                                     "ChargedPfoLooseTimingCut": ["3"],
                                     "ChargedPfoNegativeLooseTimingCut": ["-2.0"],
                                     "ChargedPfoNegativeTightTimingCut": ["-2.0"],
                                     "ChargedPfoPtCut": ["0"],
                                     "ChargedPfoPtCutForLooseTiming": ["4"],
                                     "ChargedPfoTightTimingCut": ["1.5"],
                                     "CheckKaonCorrection": ["0"],
                                     "CheckProtonCorrection": ["0"],
                                     "ClusterLessPfoTrackTimeCut": ["1000."],
                                     "CorrectHitTimesForTimeOfFlight": ["0"],
                                     "DisplayRejectedPfos": ["1"],
                                     "DisplaySelectedPfos": ["1"],
                                     "FarForwardCosTheta": ["0.975"],
                                     "ForwardCosThetaForHighEnergyNeutralHadrons": ["0.95"],
                                     "ForwardHighEnergyNeutralHadronsEnergy": ["10"],
                                     "HCalBarrelLooseTimingCut": ["20"],
                                     "HCalBarrelTightTimingCut": ["10"],
                                     "HCalEndCapTimingFactor": ["1"],
                                     "InputPfoCollection": ["PandoraPFOs"],
                                     "KeepKShorts": ["1"],
                                     "MaxMomentumForClusterLessPfos": ["2"],
                                     "MinECalHitsForTiming": ["5"],
                                     "MinHCalEndCapHitsForTiming": ["5"],
                                     "MinMomentumForClusterLessPfos": ["0.0"],
                                     "MinPtForClusterLessPfos": ["0.25"],
                                     "MinimumEnergyForNeutronTiming": ["1"],
                                     "Monitoring": ["0"],
                                     "MonitoringPfoEnergyToDisplay": ["1"],
                                     "NeutralFarForwardLooseTimingCut": ["2.5"],
                                     "NeutralFarForwardTightTimingCut": ["1.5"],
                                     "NeutralHadronBarrelPtCutForLooseTiming": ["3.5"],
                                     "NeutralHadronLooseTimingCut": ["2.5"],
                                     "NeutralHadronPtCut": ["0"],
                                     "NeutralHadronPtCutForLooseTiming": ["8"],
                                     "NeutralHadronTightTimingCut": ["1.5"],
                                     "PhotonFarForwardLooseTimingCut": ["2"],
                                     "PhotonFarForwardTightTimingCut": ["1"],
                                     "PhotonLooseTimingCut": ["2."],
                                     "PhotonPtCut": ["0"],
                                     "PhotonPtCutForLooseTiming": ["4"],
                                     "PhotonTightTimingCut": ["2."],
                                     "PtCutForTightTiming": ["0.75"],
                                     "SelectedPfoCollection": ["LooseSelectedPandoraPFOs"],
                                     "UseClusterLessPfos": ["1"],
                                     "UseNeutronTiming": ["0"]
                                     }

MyCLICPfoSelectorTight = MarlinProcessorWrapper("MyCLICPfoSelectorTight")
MyCLICPfoSelectorTight.OutputLevel = WARNING
MyCLICPfoSelectorTight.ProcessorType = "CLICPfoSelector"
MyCLICPfoSelectorTight.Parameters = {
                                     "ChargedPfoLooseTimingCut": ["2.0"],
                                     "ChargedPfoNegativeLooseTimingCut": ["-0.5"],
                                     "ChargedPfoNegativeTightTimingCut": ["-0.25"],
                                     "ChargedPfoPtCut": ["0"],
                                     "ChargedPfoPtCutForLooseTiming": ["4"],
                                     "ChargedPfoTightTimingCut": ["1.0"],
                                     "CheckKaonCorrection": ["0"],
                                     "CheckProtonCorrection": ["0"],
                                     "ClusterLessPfoTrackTimeCut": ["10"],
                                     "CorrectHitTimesForTimeOfFlight": ["0"],
                                     "DisplayRejectedPfos": ["1"],
                                     "DisplaySelectedPfos": ["1"],
                                     "FarForwardCosTheta": ["0.95"],
                                     "ForwardCosThetaForHighEnergyNeutralHadrons": ["0.95"],
                                     "ForwardHighEnergyNeutralHadronsEnergy": ["10"],
                                     "HCalBarrelLooseTimingCut": ["20"],
                                     "HCalBarrelTightTimingCut": ["10"],
                                     "HCalEndCapTimingFactor": ["1"],
                                     "InputPfoCollection": ["PandoraPFOs"],
                                     "KeepKShorts": ["1"],
                                     "MaxMomentumForClusterLessPfos": ["1.5"],
                                     "MinECalHitsForTiming": ["5"],
                                     "MinHCalEndCapHitsForTiming": ["5"],
                                     "MinMomentumForClusterLessPfos": ["0.5"],
                                     "MinPtForClusterLessPfos": ["1.0"],
                                     "MinimumEnergyForNeutronTiming": ["1"],
                                     "Monitoring": ["0"],
                                     "MonitoringPfoEnergyToDisplay": ["1"],
                                     "NeutralFarForwardLooseTimingCut": ["1.5"],
                                     "NeutralFarForwardTightTimingCut": ["1"],
                                     "NeutralHadronBarrelPtCutForLooseTiming": ["3.5"],
                                     "NeutralHadronLooseTimingCut": ["2.5"],
                                     "NeutralHadronPtCut": ["0.5"],
                                     "NeutralHadronPtCutForLooseTiming": ["8"],
                                     "NeutralHadronTightTimingCut": ["1.5"],
                                     "PhotonFarForwardLooseTimingCut": ["2"],
                                     "PhotonFarForwardTightTimingCut": ["1"],
                                     "PhotonLooseTimingCut": ["2"],
                                     "PhotonPtCut": ["0.2"],
                                     "PhotonPtCutForLooseTiming": ["4"],
                                     "PhotonTightTimingCut": ["1"],
                                     "PtCutForTightTiming": ["1.0"],
                                     "SelectedPfoCollection": ["TightSelectedPandoraPFOs"],
                                     "UseClusterLessPfos": ["0"],
                                     "UseNeutronTiming": ["0"]
                                     }

PFOSelectorSequence = [
    MyCLICPfoSelectorDefault,
    MyCLICPfoSelectorLoose,
    MyCLICPfoSelectorTight,
]
