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

# File: cld_arc_steer.py
# Description: this file extends the ddsim steering file used for CLD
#              with the specifications to run the ARC subdetector
#

# First, load cld steering file

from cld_steer import *
# change the compact file to the CLD option 3 (which contains ARC)
SIM.compactFile = os.environ["K4GEO"]+"/FCCee/CLD/compact/CLD_o3_v01/CLD_o3_v01.xml"

# Second, define specifications for ARC:

# Register optical physics and Cerenkov process to the default physics
def setupCerenkov(kernel):
        from DDG4 import PhysicsList

        seq = kernel.physicsList()
        cerenkov = PhysicsList(kernel, "Geant4CerenkovPhysics/CerenkovPhys")
        cerenkov.MaxNumPhotonsPerStep = 10
        cerenkov.MaxBetaChangePerStep = 10.0
        cerenkov.TrackSecondariesFirst = False
        cerenkov.VerboseLevel = 0
        cerenkov.enableUI()
        seq.adopt(cerenkov)
        ph = PhysicsList(kernel, "Geant4OpticalPhotonPhysics/OpticalGammaPhys")
        ph.addParticleConstructor("G4OpticalPhoton")
        ph.VerboseLevel = 0
        ph.BoundaryInvokeSD = True
        ph.enableUI()
        seq.adopt(ph)
        return None
SIM.physics.setupUserPhysics(setupCerenkov)

# Associate the Geant4OpticalTrackerAction to these detectors
# this action register total energy of the opt photon as a single hit
# and kills the optical photon, so no time is wasted tracking them
SIM.action.mapActions["ARCBARREL"] = "Geant4OpticalTrackerAction"
SIM.action.mapActions["ARCENDCAP"] = "Geant4OpticalTrackerAction"

# Define filter, so detector is only sensitive to optical photons
SIM.filter.filters["opticalphotons"] = dict(
        name="ParticleSelectFilter/OpticalPhotonSelector",
        parameter={"particle": "opticalphoton"},
        )
SIM.filter.mapDetFilter["ARCBARREL"] = "opticalphotons"
SIM.filter.mapDetFilter["ARCENDCAP"] = "opticalphotons"
