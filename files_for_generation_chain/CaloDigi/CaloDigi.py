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


MyDDCaloDigiParameters = {
                                "Histograms": ["0"],
                                "RootFile": ["Digi_SiW.root"],
                                "RelationOutputCollection": ["RelationCaloHit"],
                                "energyPerEHpair": ["3.6"],
                                # ECAL
                                "ECALCollections": ["ECalBarrelCollection", "ECalEndcapCollection"],
                                "ECALOutputCollection0": ["ECALBarrel"],
                                "ECALOutputCollection1": ["ECALEndcap"],
                                "ECALOutputCollection2": [""],
                                "IfDigitalEcal": ["0"],
                                "ECALLayers": ["41", "100"],
                                "ECAL_default_layerConfig": ["000000000000000"],
                                "StripEcal_default_nVirtualCells": ["9"],
                                "CalibECALMIP": ["0.0001"],
                                "ECALThreshold": ["5e-05"],
                                "ECALThresholdUnit": ["GeV"],
                                "ECALGapCorrection": ["1"],
                                "ECALGapCorrectionFactor": ["1"],
                                "ECALModuleGapCorrectionFactor": ["0.0"],
                                "MapsEcalCorrection": ["0"],
                                "ECAL_PPD_N_Pixels": ["10000"],
                                "ECAL_PPD_N_Pixels_uncertainty": ["0.05"],
                                "ECAL_PPD_PE_per_MIP": ["7"],
                                "ECAL_apply_realistic_digi": ["0"],
                                "ECAL_deadCellRate": ["0"],
                                "ECAL_deadCell_memorise": ["false"],
                                "ECAL_elec_noise_mips": ["0"],
                                "ECAL_maxDynamicRange_MIP": ["2500"],
                                "ECAL_miscalibration_correl": ["0"],
                                "ECAL_miscalibration_uncorrel": ["0"],
                                "ECAL_miscalibration_uncorrel_memorise": ["false"],
                                "ECAL_pixel_spread": ["0.05"],
                                "ECAL_strip_absorbtionLength": ["1e+06"],
                                "UseEcalTiming": ["1"],
                                "ECALCorrectTimesForPropagation": ["1"],
                                "ECALTimeWindowMin": ["-1"],
                                "ECALSimpleTimingCut": ["true"],
                                "ECALDeltaTimeHitResolution": ["10"],
                                "ECALTimeResolution": ["10"],
                                # HCAL
                                "HCALCollections": ["HCalBarrelCollection", "HCalEndcapCollection", "HCalRingCollection"],
                                "HCALOutputCollection0": ["HCALBarrel"],
                                "HCALOutputCollection1": ["HCALEndcap"],
                                "HCALOutputCollection2": ["HCALOther"],
                                "IfDigitalHcal": ["0"],
                                "HCALLayers": ["100"],
                                "CalibHCALMIP": ["0.0001"],
                                "HCALThreshold": ["0.00025"],
                                "HCALThresholdUnit": ["GeV"],
                                "HCALEndcapCorrectionFactor": ["1.000"],
                                "HCALGapCorrection": ["1"],
                                "HCALModuleGapCorrectionFactor": ["0.5"],
                                "HCAL_PPD_N_Pixels": ["400"],
                                "HCAL_PPD_N_Pixels_uncertainty": ["0.05"],
                                "HCAL_PPD_PE_per_MIP": ["10"],
                                "HCAL_apply_realistic_digi": ["0"],
                                "HCAL_deadCellRate": ["0"],
                                "HCAL_deadCell_memorise": ["false"],
                                "HCAL_elec_noise_mips": ["0"],
                                "HCAL_maxDynamicRange_MIP": ["200"],
                                "HCAL_miscalibration_correl": ["0"],
                                "HCAL_miscalibration_uncorrel": ["0"],
                                "HCAL_miscalibration_uncorrel_memorise": ["false"],
                                "HCAL_pixel_spread": ["0"],
                                "UseHcalTiming": ["1"],
                                "HCALCorrectTimesForPropagation": ["1"],
                                "HCALTimeWindowMin": ["-1"],
                                "HCALSimpleTimingCut": ["true"],
                                "HCALDeltaTimeHitResolution": ["10"],
                                "HCALTimeResolution": ["10"],
}

MyDDCaloDigi = {}

MyDDCaloDigi["10ns"] = MarlinProcessorWrapper("MyDDCaloDigi_10ns")
MyDDCaloDigi["10ns"].OutputLevel = WARNING
MyDDCaloDigi["10ns"].ProcessorType = "DDCaloDigi"
MyDDCaloDigi["10ns"].Parameters = MyDDCaloDigiParameters.copy()
MyDDCaloDigi["10ns"].Parameters |= {
                                "CalibrECAL": ["37.5227197175", "37.5227197175"],
                                "ECALEndcapCorrectionFactor": ["1.03245503522"],
                                "ECALBarrelTimeWindowMax": ["10"],
                                "ECALEndcapTimeWindowMax": ["10"],
                                "CalibrHCALBarrel": ["45.9956826061"],
                                "CalibrHCALEndcap": ["46.9252540291"],
                                "CalibrHCALOther": ["57.4588011802"],
                                "HCALBarrelTimeWindowMax": ["10"],
                                "HCALEndcapTimeWindowMax": ["10"],
                                }

MyDDCaloDigi["400ns"] = MarlinProcessorWrapper("MyDDCaloDigi_400ns")
MyDDCaloDigi["400ns"].OutputLevel = WARNING
MyDDCaloDigi["400ns"].ProcessorType = "DDCaloDigi"
MyDDCaloDigi["400ns"].Parameters = MyDDCaloDigiParameters.copy()
MyDDCaloDigi["400ns"].Parameters |= {
                                 "CalibrECAL": ["37.4591745147", "37.4591745147"],
                                 "ECALEndcapCorrectionFactor": ["1.01463983425"],
                                 "ECALBarrelTimeWindowMax": ["400"],
                                 "ECALEndcapTimeWindowMax": ["400"],
                                 "CalibrHCALBarrel": ["42.544403752"],
                                 "CalibrHCALEndcap": ["42.9667604345"],
                                 "CalibrHCALOther": ["51.3503963688"],
                                 "HCALBarrelTimeWindowMax": ["400"],
                                 "HCALEndcapTimeWindowMax": ["400"],
                                 }

CaloDigiSequence = [
    MyDDCaloDigi[CONFIG["CalorimeterIntegrationTimeWindow"]]
]
