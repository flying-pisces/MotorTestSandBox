#!/usr/bin/env python3
"""
Standalone FreeCAD Parameter Report Generator
This script can run independently to show parameters and generate a FreeCAD macro
"""

# Import the parameters from the main script
import sys
import os

# Add current directory to path to import FreeCAD_Parameters
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import just the parameters (without FreeCAD dependencies)
DESIGN_PARAMETERS = {
    # Base Frame Parameters
    'base_length': 800.0,           # mm
    'base_width': 600.0,            # mm  
    'base_height': 150.0,           # mm
    'base_material': 'Cast_Iron_GG25',
    'base_mass': 180.0,             # kg (estimated)
    
    # Motor Specifications (ILM-E85x30)
    'motor_stator_diameter': 85.0,  # mm
    'motor_stator_length': 44.4,    # mm
    'motor_rotor_bore': 52.0,       # mm (H8 tolerance)
    'motor_rotor_length': 31.2,     # mm
    'motor_mass': 0.822,            # kg
    'motor_rated_torque': 3.3,      # Nm
    'motor_peak_torque': 10.64,     # Nm
    'motor_max_speed': 2570,        # rpm
    
    # Motor Housing Parameters
    'housing_outer_diameter': 150.0, # mm
    'housing_length': 80.0,          # mm
    'housing_bore_diameter': 85.0,   # mm (U6 fit: -0.117/-0.139)
    'housing_bore_tolerance': 'U6',
    'housing_material': 'Aluminum_6061_T6',
    'housing_cooling_fins': True,
    'housing_fin_height': 15.0,      # mm
    'housing_fin_count': 12,
    
    # Shaft System Parameters
    'shaft_diameter': 50.0,          # mm (fits in 52mm rotor bore)
    'shaft_length': 400.0,           # mm
    'shaft_material': 'Tool_Steel_D2',
    'shaft_hardness': 'HRC_58-62',
    'shaft_surface_finish': 0.4,     # Ra in μm
    
    # Bearing Specifications
    'bearing_type': 'SKF_7010',
    'bearing_bore': 50.0,            # mm
    'bearing_outer_diameter': 80.0,  # mm
    'bearing_width': 16.0,           # mm
    'bearing_precision_grade': 'P4',
    
    # Torque Sensor Parameters
    'sensor_model': 'HBK_T210_10Nm',
    'sensor_range': 10.0,           # Nm
    'sensor_accuracy': 0.1,         # %
    'sensor_length': 150.0,         # mm (estimated)
    'sensor_input_shaft': 25.0,     # mm diameter
    'sensor_output_shaft': 25.0,    # mm diameter
    
    # Load System Parameters
    'load_type': 'Hysteresis_Brake',
    'load_torque_capacity': 15.0,   # Nm
    'load_speed_capacity': 5000,    # rpm
    'load_cooling': 'Air_Cooled',
    
    # Safety Factors
    'torque_safety_factor': 1.5,
    'speed_safety_factor': 2.0,
    'structural_safety_factor': 3.0,
    
    # Tolerance and Precision
    'alignment_tolerance': 0.02,     # mm TIR
    'parallelism_tolerance': 0.05,   # mm
    'position_repeatability': 0.01,  # mm
    
    # Control System Parameters
    'motor_drive_voltage': 48.0,     # V
    'motor_drive_current': 25.0,     # A
    'data_acquisition_rate': 1000,   # Hz
    'temperature_sensors': 6,        # count
    
    # Environmental Conditions
    'operating_temp_min': 15.0,      # °C
    'operating_temp_max': 40.0,      # °C
    'humidity_max': 80.0,            # % RH
    'vibration_isolation_freq': 5.0, # Hz (natural frequency)
}

def generate_parameter_report():
    """Generate a comprehensive report of all design parameters"""
    print("="*60)
    print("FREECAD PARAMETRIC DESIGN PARAMETERS")
    print("ILM-E85x30 Motor Test Bed - Assignment 1")
    print("="*60)
    
    categories = {
        'Base Frame': ['base_length', 'base_width', 'base_height', 'base_material', 'base_mass'],
        'Motor Specifications': ['motor_stator_diameter', 'motor_stator_length', 'motor_rotor_bore', 
                                'motor_rated_torque', 'motor_peak_torque', 'motor_max_speed'],
        'Motor Housing': ['housing_outer_diameter', 'housing_length', 'housing_material', 
                         'housing_cooling_fins', 'housing_fin_count'],
        'Shaft System': ['shaft_diameter', 'shaft_length', 'shaft_material', 'shaft_hardness'],
        'Bearing System': ['bearing_type', 'bearing_bore', 'bearing_outer_diameter', 'bearing_precision_grade'],
        'Torque Sensor': ['sensor_model', 'sensor_range', 'sensor_accuracy', 'sensor_length'],
        'Load System': ['load_type', 'load_torque_capacity', 'load_speed_capacity'],
        'Critical Tolerances': ['alignment_tolerance', 'parallelism_tolerance', 'position_repeatability'],
        'Safety Factors': ['torque_safety_factor', 'speed_safety_factor', 'structural_safety_factor']
    }
    
    for category, params in categories.items():
        print(f"\n{category}:")
        for param in params:
            if param in DESIGN_PARAMETERS:
                value = DESIGN_PARAMETERS[param]
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                print(f"  {param}: {value}")
    
    print("="*60)
    print(f"Total Parameters Defined: {len(DESIGN_PARAMETERS)}")
    
    # Calculate some derived values
    print(f"\nDerived Design Values:")
    motor_volume = (DESIGN_PARAMETERS['motor_stator_diameter']**2 * 3.14159 * 
                   DESIGN_PARAMETERS['motor_stator_length'] / 4) / 1000000  # cm³
    print(f"  Motor Volume: {motor_volume:.1f} cm³")
    
    torque_density = DESIGN_PARAMETERS['motor_rated_torque'] / DESIGN_PARAMETERS['motor_mass']
    print(f"  Torque Density: {torque_density:.2f} Nm/kg")
    
    safety_torque_max = DESIGN_PARAMETERS['sensor_range'] * 0.8  # 80% of sensor range
    print(f"  Safe Torque Range: 0-{safety_torque_max:.1f} Nm")
    
    shaft_clearance = (DESIGN_PARAMETERS['motor_rotor_bore'] - DESIGN_PARAMETERS['shaft_diameter']) / 2
    print(f"  Shaft-to-Rotor Clearance: {shaft_clearance:.1f} mm per side")
    
    print("="*60)

def generate_freecad_macro():
    """Generate a FreeCAD macro file that can be run directly in FreeCAD"""
    macro_content = '''# FreeCAD Macro: Motor Test Bed Generator
# Generated from Assignment 1 parametric design
# Usage: Open FreeCAD, run this macro from Macro menu

import FreeCAD as App
import Part
import PartDesign

# Design Parameters
DESIGN_PARAMETERS = ''' + str(DESIGN_PARAMETERS) + '''

def create_base_frame():
    """Create the main base frame for the test bed"""
    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument("MotorTestBed")
    
    # Create base frame body
    base = doc.addObject("Part::Box", "BaseFrame")
    base.Length = DESIGN_PARAMETERS['base_length']
    base.Width = DESIGN_PARAMETERS['base_width']
    base.Height = DESIGN_PARAMETERS['base_height']
    base.Placement = App.Placement(
        App.Vector(-DESIGN_PARAMETERS['base_length']/2, 
                  -DESIGN_PARAMETERS['base_width']/2, 0),
        App.Rotation(0, 0, 0, 1)
    )
    
    doc.recompute()
    return base

def create_motor_housing():
    """Create the aluminum housing for the motor stator"""
    doc = App.ActiveDocument
    
    # Outer housing cylinder
    outer_cylinder = doc.addObject("Part::Cylinder", "HousingOuter")
    outer_cylinder.Radius = DESIGN_PARAMETERS['housing_outer_diameter'] / 2
    outer_cylinder.Height = DESIGN_PARAMETERS['housing_length']
    outer_cylinder.Placement = App.Placement(
        App.Vector(0, 0, DESIGN_PARAMETERS['base_height']),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Inner bore for stator
    inner_cylinder = doc.addObject("Part::Cylinder", "HousingBore")
    inner_cylinder.Radius = DESIGN_PARAMETERS['housing_bore_diameter'] / 2
    inner_cylinder.Height = DESIGN_PARAMETERS['housing_length'] + 10  # Through hole
    inner_cylinder.Placement = App.Placement(
        App.Vector(0, 0, DESIGN_PARAMETERS['base_height'] - 5),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Create housing with bore
    housing = doc.addObject("Part::Cut", "MotorHousing")
    housing.Base = outer_cylinder
    housing.Tool = inner_cylinder
    
    doc.recompute()
    return housing

def create_shaft():
    """Create the main shaft"""
    doc = App.ActiveDocument
    
    shaft = doc.addObject("Part::Cylinder", "MainShaft")
    shaft.Radius = DESIGN_PARAMETERS['shaft_diameter'] / 2
    shaft.Height = DESIGN_PARAMETERS['shaft_length']
    shaft.Placement = App.Placement(
        App.Vector(0, 0, DESIGN_PARAMETERS['base_height'] - DESIGN_PARAMETERS['shaft_length']/4),
        App.Rotation(0, 0, 0, 1)
    )
    
    doc.recompute()
    return shaft

def create_sensor_mount():
    """Create sensor mounting plate"""
    doc = App.ActiveDocument
    
    mount = doc.addObject("Part::Box", "SensorMount")
    mount.Length = 200
    mount.Width = 150
    mount.Height = 25
    mount.Placement = App.Placement(
        App.Vector(50, -75, DESIGN_PARAMETERS['base_height']),
        App.Rotation(0, 0, 0, 1)
    )
    
    doc.recompute()
    return mount

def generate_assembly():
    """Generate the complete test bed assembly"""
    print("Generating Motor Test Bed Assembly in FreeCAD...")
    
    # Create new document
    doc = App.newDocument("MotorTestBed")
    
    # Create components
    base = create_base_frame()
    housing = create_motor_housing()
    shaft = create_shaft()
    sensor_mount = create_sensor_mount()
    
    # Set materials (as labels)
    base.Label = "Base Frame (Cast Iron)"
    housing.Label = "Motor Housing (Al 6061-T6)"
    shaft.Label = "Main Shaft (Tool Steel D2)"
    sensor_mount.Label = "Sensor Mount (Steel)"
    
    # Color components
    base.ViewObject.ShapeColor = (0.5, 0.5, 0.5)      # Gray
    housing.ViewObject.ShapeColor = (0.8, 0.8, 0.9)    # Light Blue
    shaft.ViewObject.ShapeColor = (0.9, 0.9, 0.7)      # Light Yellow  
    sensor_mount.ViewObject.ShapeColor = (0.7, 0.7, 0.9) # Light Purple
    
    doc.recompute()
    
    # Fit view
    App.Gui.SendMsgToActiveView("ViewFit")
    
    print("Assembly generation complete!")
    print(f"Components created:")
    print(f"  - Base Frame: {DESIGN_PARAMETERS['base_length']}x{DESIGN_PARAMETERS['base_width']}x{DESIGN_PARAMETERS['base_height']} mm")
    print(f"  - Motor Housing: Ø{DESIGN_PARAMETERS['housing_outer_diameter']}mm x {DESIGN_PARAMETERS['housing_length']}mm")
    print(f"  - Main Shaft: Ø{DESIGN_PARAMETERS['shaft_diameter']}mm x {DESIGN_PARAMETERS['shaft_length']}mm")
    print(f"  - Torque Sensor: {DESIGN_PARAMETERS['sensor_model']}")
    
    return doc

# Run the assembly generation
if __name__ == "__main__":
    generate_assembly()
'''
    
    with open('MotorTestBed_FreeCAD_Macro.FCMacro', 'w') as f:
        f.write(macro_content)
    
    print(f"\n✅ FreeCAD Macro Generated: MotorTestBed_FreeCAD_Macro.FCMacro")
    print("To use:")
    print("1. Open FreeCAD")
    print("2. Go to Macro → Macros...")
    print("3. Load and execute this macro file")
    print("4. The complete test bed assembly will be generated")

def generate_openscad_model():
    """Generate an OpenSCAD model as alternative CAD approach"""
    openscad_content = '''// OpenSCAD Model: ILM-E85x30 Motor Test Bed
// Generated from Assignment 1 parametric design
// Usage: Open in OpenSCAD and render

$fn = 50; // Smooth curves

// Design Parameters
base_length = ''' + str(DESIGN_PARAMETERS['base_length']) + ''';
base_width = ''' + str(DESIGN_PARAMETERS['base_width']) + ''';
base_height = ''' + str(DESIGN_PARAMETERS['base_height']) + ''';

housing_outer_dia = ''' + str(DESIGN_PARAMETERS['housing_outer_diameter']) + ''';
housing_length = ''' + str(DESIGN_PARAMETERS['housing_length']) + ''';
housing_bore_dia = ''' + str(DESIGN_PARAMETERS['housing_bore_diameter']) + ''';

shaft_diameter = ''' + str(DESIGN_PARAMETERS['shaft_diameter']) + ''';
shaft_length = ''' + str(DESIGN_PARAMETERS['shaft_length']) + ''';

// Colors
color_base = [0.5, 0.5, 0.5];      // Gray (Cast Iron)
color_housing = [0.8, 0.8, 0.9];   // Light Blue (Aluminum)
color_shaft = [0.9, 0.9, 0.7];     // Light Yellow (Steel)
color_mount = [0.7, 0.7, 0.9];     // Light Purple

module base_frame() {
    color(color_base)
    translate([-base_length/2, -base_width/2, 0])
    cube([base_length, base_width, base_height]);
}

module motor_housing() {
    color(color_housing)
    translate([0, 0, base_height])
    difference() {
        cylinder(d=housing_outer_dia, h=housing_length);
        translate([0, 0, -1])
        cylinder(d=housing_bore_dia, h=housing_length+2);
    }
}

module main_shaft() {
    color(color_shaft)
    translate([0, 0, base_height - shaft_length/4])
    cylinder(d=shaft_diameter, h=shaft_length);
}

module sensor_mount() {
    color(color_mount)
    translate([50, -75, base_height])
    cube([200, 150, 25]);
}

module cooling_fins() {
    color(color_housing)
    translate([0, 0, base_height])
    for(i = [0:30:330]) {
        rotate([0, 0, i])
        translate([housing_outer_dia/2, -2.5, 0])
        cube([15, 5, housing_length]);
    }
}

// Assembly
module motor_test_bed() {
    base_frame();
    motor_housing();
    cooling_fins();
    main_shaft();
    sensor_mount();
}

// Generate the complete assembly
motor_test_bed();

// Add text labels
translate([0, -base_width/2 - 50, 0])
color([0, 0, 0])
text("ILM-E85x30 Motor Test Bed", size=20, halign="center");

translate([0, -base_width/2 - 80, 0])
color([0, 0, 0])
text("Assignment 1 - Parametric Design", size=12, halign="center");
'''
    
    with open('MotorTestBed_OpenSCAD.scad', 'w') as f:
        f.write(openscad_content)
    
    print(f"✅ OpenSCAD Model Generated: MotorTestBed_OpenSCAD.scad")
    print("To use:")
    print("1. Open OpenSCAD")
    print("2. Load this .scad file")
    print("3. Press F5 to preview or F6 to render")

if __name__ == "__main__":
    # Generate parameter report
    generate_parameter_report()
    
    # Generate FreeCAD macro
    generate_freecad_macro()
    
    # Generate OpenSCAD model
    generate_openscad_model()
    
    print(f"\n🎯 CAD GENERATION COMPLETE!")
    print(f"Generated files ready for both FreeCAD and OpenSCAD")
    print(f"All based on {len(DESIGN_PARAMETERS)} parametric design parameters")