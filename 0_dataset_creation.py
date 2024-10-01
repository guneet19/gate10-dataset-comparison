# This file replicates the dataset creation testfile
# of Gate 9

import opengate as gate
import opengate.tests.utility as tu

if __name__ == "__main__":
    paths = tu.get_default_test_paths(__file__, "")
    paths.data = paths.current

    print(f"The information insides paths variable is {paths}")

    # create simulation
    sim = gate.Simulation()
    sim.g4_verbose = True

    # units
    m = gate.g4_units.m
    cm = gate.g4_units.cm
    mm = gate.g4_units.mm
    um = gate.g4_units.um
    eV = gate.g4_units.eV
    MeV = gate.g4_units.MeV
    keV = gate.g4_units.keV
    Bq = gate.g4_units.Bq
    deg = gate.g4_units.deg

    # set the world size like in the Gate macro
    # verified with C++ macro files
    sim.world.size = [10 * cm, 10 * cm, 15 * cm]

    # optical_system 
    # verified with C++ macro files 
    optical_system = sim.add_volume("Box", "optical_system")
    optical_system.size = [10 * cm, 10 * cm, 14 * cm]
    optical_system.material = "G4_AIR"
    optical_system.translation = [0 * cm, 0 * cm, 0 * cm]

    # add a material database
    sim.volume_manager.add_material_database(paths.data / "GateMaterials.db")

    # crystal 
    # verified with C++ macro files
    crystal = sim.add_volume("Box", "crystal")
    crystal.attached_to = optical_system.name
    crystal.size = [3 * mm, 3 * mm, 20 * mm]
    crystal.translation = [0 * mm, 0 * mm, 10 * mm]
    crystal.material = "BGO"

    # grease
    # verified with C++ macro files
    grease = sim.add_volume("Box", "grease")
    grease.attached_to = optical_system.name
    grease.size = [3 * mm, 3 * mm, 0.015 * mm]
    grease.material = "Epoxy"
    grease.translation = [0 * mm, 0 * mm, 20.0075 * mm]

    # pixel
    # verified with C++ macro files 
    pixel = sim.add_volume("Box", "pixel")
    pixel.attached_to = optical_system.name
    pixel.size = [3 * mm, 3 * mm, 0.1 * mm]
    pixel.material = "SiO2"
    pixel.translation = [0 * mm, 0 * mm, 20.065 * mm]

    # physics
    # verified with C++ macro files
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
    sim.physics_manager.set_production_cut("world", "electron", 10 * mm) #same as SetCutInRegion?
    sim.physics_manager.set_production_cut("world", "positron", 10 * um)
    sim.physics_manager.set_production_cut("crystal", "electron", 10 * um)
    sim.physics_manager.set_production_cut("crystal", "positron", 10 * um)
    sim.physics_manager.energy_range_min = 10 * eV
    sim.physics_manager.energy_range_max = 1 * MeV
    sim.physics_manager.special_physics_constructors.G4OpticalPhysics = True

    # surfaces
    # verified with C++ macro files

    # RoughESR_LUT.z -> Customized3_LUT.z
    # RoughESR_LUTR.z -> Customized3_LUTR.z
    opt_surf_optical_system_to_crystal = sim.physics_manager.add_optical_surface(
        volume_from="optical_system",
        volume_to="crystal",
        g4_surface_name="RoughESR_LUT",
    )

    opt_surf_crystal_to_optical_system = sim.physics_manager.add_optical_surface(
        "crystal", "optical_system", "RoughESR_LUT"
    )

    # Rough_LUT.z -> Customized2_LUT.z
    # Rough_LUTR.z -> Customized2_LUTR.z
    opt_surf_grease_to_crystal = sim.physics_manager.add_optical_surface("grease", "crystal", "Rough_LUT")

    opt_surf_crystal_to_grease = sim.physics_manager.add_optical_surface("crystal", "grease", "Rough_LUT")

    # RoughESRGrease_LUT.z -> Customized4_LUT.z
    # RoughESRGrease_LUTR.z -> Customized4_LUTR.z
    opt_surface_pixel_to_grease = sim.physics_manager.add_optical_surface("pixel", "grease", "RoughESRGrease_LUT")

    opt_surf_grease_to_pixel = sim.physics_manager.add_optical_surface("grease", "pixel", "RoughESRGrease_LUT")

    # source user info
    # verified with C++ macro files
    source = sim.add_source("GenericSource", "my_source")
    source.particle = "e-"
    source.energy.type = "mono"
    source.energy.mono = 420 * keV
    source.position.type = "sphere"
    source.position.radius = 0 * mm
    source.activity = 10 * Bq
    source.direction.type = "iso"
    source.direction.theta = [163 * deg, 165 * deg]
    source.direction.phi = [100 * deg, 110 * deg]
    source.position.translation = [0 * mm, 0 * mm, 19 * mm]

    # add a phase space actor to the crystal
    # verified with C++ macro files 
    phase = sim.add_actor("PhaseSpaceActor", "Phase")
    phase.attached_to = pixel.name
    phase.output = paths.output / "test075_optigan_create_dataset.root"
    phase.attributes = [
        "EventID",
        "ParticleName",
        "Position",
        "TrackID",
        "ParentID",
        "Direction",
        "KineticEnergy",
        "LocalTime",
        "GlobalTime",
        "TimeFromBeginOfEvent",
        "StepLength",
        "TrackCreatorProcess",
        "TrackLength",
        "PDGCode",
    ]

    # optical_adder = sim.add_actor("HitsReadoutActor", "Singles")
    # optical_adder.input_digi_collection = "Hits"

    sim.user_hook_after_run = gate.userhooks.user_hook_dump_material_properties
    sim.run()

    is_ok = all(t is True for t in sim.output.hook_log)
    tu.test_ok(is_ok)
