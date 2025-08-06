#!/usr/bin/env python3
"""
FUTEK-Style Horizontal Motor Test Bench - FreeCAD Macro
Professional horizontal configuration based on Example 2 reference

Motor → Torque Sensor → Eddy Current Brake

This macro creates a complete parametric assembly in FreeCAD
following professional motor test bench design practices.
"""

import FreeCAD as App
import Part
import PartDesign

# Import parameters
FUTEK_PARAMETERS = {
    # Base Platform Parameters
    'base_length': 1000.0,          # mm
    'base_width': 400.0,            # mm  
    'base_height': 20.0,            # mm
    'base_material': 'Aluminum_6061_T6',
    
    # Motor Integration (Left Side)
    'motor_position_x': 150.0,      # mm from left edge
    'motor_mount_height': 100.0,    # mm above base
    'motor_stator_diameter': 85.0,  # mm - ILM-E85x30
    'motor_stator_length': 44.4,    # mm
    'motor_rotor_bore': 52.0,       # mm
    'motor_shaft_extension': 50.0,  # mm beyond stator
    
    # Torque Sensor (Center)
    'sensor_position_x': 500.0,     # mm from left edge
    'sensor_type': 'FUTEK_TRS600',
    'sensor_length': 100.0,         # mm
    'sensor_diameter': 50.0,        # mm body diameter
    'sensor_shaft_diameter': 25.0,  # mm input/output shafts
    
    # Eddy Current Brake (Right Side)
    'brake_position_x': 850.0,      # mm from left edge
    'brake_disc_diameter': 200.0,   # mm
    'brake_disc_thickness': 30.0,   # mm
    'brake_housing_width': 150.0,   # mm
    'brake_housing_height': 120.0,  # mm
    'brake_fin_count': 24,          # cooling fins
    
    # Shaft System
    'main_shaft_diameter': 25.0,    # mm
    'main_shaft_length': 600.0,     # mm
    
    # Bearing Pedestals
    'pedestal_count': 4,            # Motor, sensor×2, brake
    'pedestal_height': 100.0,       # mm
    'pedestal_width': 80.0,         # mm
    'pedestal_depth': 120.0,        # mm
}

def create_futek_test_bench():
    """Create the complete FUTEK-style test bench assembly"""
    
    # Create new document
    doc = App.newDocument("FUTEK_MotorTestBench")
    
    print("Creating FUTEK-Style Horizontal Motor Test Bench...")
    print(f"Configuration: Motor → Torque Sensor → Eddy Current Brake")
    
    # Create main components
    base_platform = create_base_platform(doc)
    motor_assembly = create_motor_assembly(doc)
    sensor_assembly = create_torque_sensor(doc) 
    brake_assembly = create_brake_assembly(doc)
    main_shaft = create_main_shaft(doc)
    pedestals = create_bearing_pedestals(doc)
    
    # Position components
    position_futek_components(base_platform, motor_assembly, sensor_assembly, 
                             brake_assembly, main_shaft, pedestals)
    
    # Set colors and materials
    apply_futek_materials(base_platform, motor_assembly, sensor_assembly, 
                         brake_assembly, main_shaft, pedestals)
    
    doc.recompute()
    
    # Fit view and show assembly
    try:
        App.Gui.SendMsgToActiveView("ViewFit")
    except:
        pass  # GUI not available in headless mode
    
    print("FUTEK-Style test bench assembly complete!")
    print_futek_summary()
    
    return doc

def create_base_platform(doc):
    """Create the main aluminum base platform"""
    
    # Main platform
    base = doc.addObject("Part::Box", "BasePlatform")
    base.Length = FUTEK_PARAMETERS['base_length']
    base.Width = FUTEK_PARAMETERS['base_width']
    base.Height = FUTEK_PARAMETERS['base_height']
    base.Placement = App.Placement(
        App.Vector(-50, -FUTEK_PARAMETERS['base_width']/2, 0),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Mounting holes
    holes = []
    for i in range(8):
        hole = doc.addObject("Part::Cylinder", f"MountingHole_{i}")
        hole.Radius = 4  # M8 clearance
        hole.Height = FUTEK_PARAMETERS['base_height'] + 2
        hole.Placement = App.Placement(
            App.Vector((i+1) * FUTEK_PARAMETERS['base_length']/9, 0, -1),
            App.Rotation(0, 0, 0, 1)
        )
        holes.append(hole)
    
    # Create platform with holes
    if holes:
        platform = doc.addObject("Part::Cut", "PlatformWithHoles")
        platform.Base = base
        platform.Tool = holes[0]
        doc.recompute()
        
        # Cut remaining holes
        for hole in holes[1:]:
            new_cut = doc.addObject("Part::Cut", f"Platform_Cut_{holes.index(hole)}")
            new_cut.Base = platform
            new_cut.Tool = hole
            platform = new_cut
            doc.recompute()
    
    return platform

def create_motor_assembly(doc):
    """Create the motor assembly (left side)"""
    
    # Motor housing (simplified ILM-E85x30)
    motor_housing = doc.addObject("Part::Cylinder", "MotorHousing")
    motor_housing.Radius = FUTEK_PARAMETERS['motor_stator_diameter'] / 2
    motor_housing.Height = FUTEK_PARAMETERS['motor_stator_length']
    motor_housing.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['motor_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)  # Horizontal orientation
    )
    
    # Motor mounting flange
    flange = doc.addObject("Part::Cylinder", "MotorFlange")
    flange.Radius = (FUTEK_PARAMETERS['motor_stator_diameter'] + 20) / 2
    flange.Height = 10
    flange.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['motor_position_x']-10, 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Motor shaft extension
    shaft_ext = doc.addObject("Part::Cylinder", "MotorShaft")
    shaft_ext.Radius = FUTEK_PARAMETERS['main_shaft_diameter'] / 2
    shaft_ext.Height = FUTEK_PARAMETERS['motor_shaft_extension']
    shaft_ext.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['motor_position_x'] + FUTEK_PARAMETERS['motor_stator_length'], 
                  0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Combine motor components
    motor_parts = doc.addObject("Part::Compound", "MotorAssembly")
    motor_parts.Links = [motor_housing, flange, shaft_ext]
    
    doc.recompute()
    return motor_parts

def create_torque_sensor(doc):
    """Create FUTEK-style torque sensor (center)"""
    
    # Sensor body
    sensor_body = doc.addObject("Part::Cylinder", "SensorBody") 
    sensor_body.Radius = FUTEK_PARAMETERS['sensor_diameter'] / 2
    sensor_body.Height = FUTEK_PARAMETERS['sensor_length']
    sensor_body.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['sensor_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Input shaft
    input_shaft = doc.addObject("Part::Cylinder", "SensorInputShaft")
    input_shaft.Radius = FUTEK_PARAMETERS['sensor_shaft_diameter'] / 2
    input_shaft.Height = 20
    input_shaft.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['sensor_position_x']-20, 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Output shaft
    output_shaft = doc.addObject("Part::Cylinder", "SensorOutputShaft")
    output_shaft.Radius = FUTEK_PARAMETERS['sensor_shaft_diameter'] / 2  
    output_shaft.Height = 20
    output_shaft.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['sensor_position_x'] + FUTEK_PARAMETERS['sensor_length'], 
                  0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Sensor label area (FUTEK branding)
    label = doc.addObject("Part::Box", "SensorLabel")
    label.Length = FUTEK_PARAMETERS['sensor_length'] * 0.6
    label.Width = 4
    label.Height = FUTEK_PARAMETERS['sensor_diameter'] * 0.8
    label.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['sensor_position_x'] + FUTEK_PARAMETERS['sensor_length']*0.2,
                  FUTEK_PARAMETERS['sensor_diameter']/2-2, 
                  FUTEK_PARAMETERS['motor_mount_height'] - FUTEK_PARAMETERS['sensor_diameter']*0.4),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Combine sensor components
    sensor_parts = doc.addObject("Part::Compound", "TorqueSensor")
    sensor_parts.Links = [sensor_body, input_shaft, output_shaft, label]
    
    doc.recompute()
    return sensor_parts

def create_brake_assembly(doc):
    """Create eddy current brake assembly (right side)"""
    
    # Brake housing
    brake_housing = doc.addObject("Part::Box", "BrakeHousing")
    brake_housing.Length = FUTEK_PARAMETERS['brake_housing_width']
    brake_housing.Width = FUTEK_PARAMETERS['brake_housing_width']
    brake_housing.Height = FUTEK_PARAMETERS['brake_housing_height']
    brake_housing.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['brake_position_x'] - FUTEK_PARAMETERS['brake_housing_width']/2,
                  -FUTEK_PARAMETERS['brake_housing_width']/2,
                  FUTEK_PARAMETERS['motor_mount_height'] - 20),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Brake disc
    brake_disc = doc.addObject("Part::Cylinder", "BrakeDisc")
    brake_disc.Radius = FUTEK_PARAMETERS['brake_disc_diameter'] / 2
    brake_disc.Height = FUTEK_PARAMETERS['brake_disc_thickness']
    brake_disc.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['brake_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Central hub
    hub = doc.addObject("Part::Cylinder", "BrakeHub")
    hub.Radius = 30
    hub.Height = FUTEK_PARAMETERS['brake_disc_thickness'] + 10
    hub.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['brake_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    # Cooling fins (simplified - few representative fins)
    fins = []
    for i in range(0, 360, 45):  # 8 fins for visualization
        fin = doc.addObject("Part::Box", f"CoolingFin_{i}")
        fin.Length = 40
        fin.Width = 3
        fin.Height = FUTEK_PARAMETERS['brake_disc_thickness'] + 10
        
        # Position fin radially
        fin_radius = FUTEK_PARAMETERS['brake_disc_diameter']/2 - 20
        fin_x = FUTEK_PARAMETERS['brake_position_x']
        fin_y = fin_radius * App.sin(App.Units.Quantity(f"{i} deg").Value)
        fin_z = FUTEK_PARAMETERS['motor_mount_height'] - (FUTEK_PARAMETERS['brake_disc_thickness']+10)/2
        
        fin.Placement = App.Placement(
            App.Vector(fin_x-20, fin_y-1.5, fin_z),
            App.Rotation(App.Vector(0,0,1), i)
        )
        fins.append(fin)
    
    # Combine brake components
    brake_parts = doc.addObject("Part::Compound", "BrakeAssembly")
    brake_parts.Links = [brake_housing, brake_disc, hub] + fins
    
    doc.recompute()
    return brake_parts

def create_main_shaft(doc):
    """Create the main shaft connecting motor to brake"""
    
    shaft_start_x = (FUTEK_PARAMETERS['motor_position_x'] + 
                     FUTEK_PARAMETERS['motor_stator_length'] + 
                     FUTEK_PARAMETERS['motor_shaft_extension'])
    shaft_length = FUTEK_PARAMETERS['brake_position_x'] - shaft_start_x
    
    main_shaft = doc.addObject("Part::Cylinder", "MainShaft")
    main_shaft.Radius = FUTEK_PARAMETERS['main_shaft_diameter'] / 2
    main_shaft.Height = shaft_length
    main_shaft.Placement = App.Placement(
        App.Vector(shaft_start_x, 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    doc.recompute()
    return main_shaft

def create_bearing_pedestals(doc):
    """Create bearing pedestals at strategic locations"""
    
    pedestals = []
    pedestal_positions = [
        FUTEK_PARAMETERS['motor_position_x'],                    # Motor side
        FUTEK_PARAMETERS['sensor_position_x'] - 60,             # Sensor input side  
        FUTEK_PARAMETERS['sensor_position_x'] + 60,             # Sensor output side
        FUTEK_PARAMETERS['brake_position_x']                     # Brake side
    ]
    
    for i, pos_x in enumerate(pedestal_positions):
        # Pedestal base
        pedestal = doc.addObject("Part::Box", f"Pedestal_{i}")
        pedestal.Length = FUTEK_PARAMETERS['pedestal_width']
        pedestal.Width = FUTEK_PARAMETERS['pedestal_depth']
        pedestal.Height = FUTEK_PARAMETERS['pedestal_height']
        pedestal.Placement = App.Placement(
            App.Vector(pos_x - FUTEK_PARAMETERS['pedestal_width']/2,
                      -FUTEK_PARAMETERS['pedestal_depth']/2,
                      FUTEK_PARAMETERS['base_height']),
            App.Rotation(0, 0, 0, 1)
        )
        
        # Bearing housing (pillow block)
        bearing_housing = doc.addObject("Part::Box", f"BearingHousing_{i}")
        bearing_housing.Length = 60
        bearing_housing.Width = 80
        bearing_housing.Height = 40
        bearing_housing.Placement = App.Placement(
            App.Vector(pos_x - 30, -40, 
                      FUTEK_PARAMETERS['base_height'] + FUTEK_PARAMETERS['pedestal_height']),
            App.Rotation(0, 0, 0, 1)
        )
        
        # Bearing bore (simplified)
        bearing_bore = doc.addObject("Part::Cylinder", f"BearingBore_{i}")
        bearing_bore.Radius = FUTEK_PARAMETERS['main_shaft_diameter']/2 + 0.5
        bearing_bore.Height = 70
        bearing_bore.Placement = App.Placement(
            App.Vector(pos_x, 0,
                      FUTEK_PARAMETERS['base_height'] + FUTEK_PARAMETERS['pedestal_height'] + 20),
            App.Rotation(App.Vector(0,1,0), 90)
        )
        
        # Cut bore from housing
        housing_with_bore = doc.addObject("Part::Cut", f"HousingWithBore_{i}")
        housing_with_bore.Base = bearing_housing
        housing_with_bore.Tool = bearing_bore
        
        pedestals.append(pedestal)
        pedestals.append(housing_with_bore)
    
    doc.recompute()
    return pedestals

def position_futek_components(base, motor, sensor, brake, shaft, pedestals):
    """Position all components correctly in the assembly"""
    # Components are positioned during creation
    # This function handles any final positioning adjustments
    pass

def apply_futek_materials(base, motor, sensor, brake, shaft, pedestals):
    """Apply colors and materials to components"""
    
    try:
        # Base platform - aluminum gray
        base.ViewObject.ShapeColor = (0.7, 0.7, 0.7)
        
        # Motor - blue
        motor.ViewObject.ShapeColor = (0.2, 0.3, 0.8)
        
        # Torque sensor - FUTEK red
        sensor.ViewObject.ShapeColor = (0.8, 0.1, 0.1)
        
        # Brake - dark gray (cast iron)
        brake.ViewObject.ShapeColor = (0.3, 0.3, 0.3)
        
        # Shaft - stainless steel
        shaft.ViewObject.ShapeColor = (0.9, 0.9, 0.8)
        
        # Pedestals - light aluminum
        for pedestal in pedestals:
            if hasattr(pedestal, 'ViewObject'):
                pedestal.ViewObject.ShapeColor = (0.8, 0.8, 0.9)
                
    except AttributeError:
        # GUI not available (headless mode)
        pass

def print_futek_summary():
    """Print assembly summary"""
    print(f"\n{'='*60}")
    print(f"FUTEK-STYLE MOTOR TEST BENCH ASSEMBLY COMPLETE")
    print(f"{'='*60}")
    print(f"Configuration: Horizontal Motor → Sensor → Brake")
    print(f"Total Length: {FUTEK_PARAMETERS['base_length']} mm")
    print(f"Motor: ILM-E85x30 at position {FUTEK_PARAMETERS['motor_position_x']} mm")
    print(f"Sensor: {FUTEK_PARAMETERS['sensor_type']} at position {FUTEK_PARAMETERS['sensor_position_x']} mm") 
    print(f"Brake: Eddy current at position {FUTEK_PARAMETERS['brake_position_x']} mm")
    print(f"Shaft Diameter: {FUTEK_PARAMETERS['main_shaft_diameter']} mm")
    print(f"Pedestals: {FUTEK_PARAMETERS['pedestal_count']} bearing supports")
    print(f"{'='*60}")

# Execute the macro
if __name__ == "__main__":
    doc = create_futek_test_bench()