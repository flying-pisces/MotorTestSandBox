#!/usr/bin/env python3
"""
FreeCAD Parametric Design Script for ILM-E85x30 Motor Test Bed
This script defines the master parameters for the test bed assembly
and provides functions to generate parametric geometry.

Usage:
1. Import this script into FreeCAD
2. Run generate_test_bed_assembly() to create the complete assembly
3. Modify parameters in DESIGN_PARAMETERS dictionary as needed

Author: Assignment 1 - Motor Test Bed Design
Date: 2025-08-04
"""

import FreeCAD as App
import Part
import PartDesign
import math

# Master Design Parameters Dictionary
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

def create_base_frame():
    """Create the main base frame for the test bed"""
    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument("MotorTestBed")
    
    # Create base frame body
    base = doc.addObject("PartDesign::Body", "BaseFrame")
    
    # Create base sketch
    sketch = base.newObject("Sketcher::SketchObject", "BaseSketch")
    sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 0))
    
    # Define base frame geometry
    length = DESIGN_PARAMETERS['base_length']
    width = DESIGN_PARAMETERS['base_width']
    
    # Create rectangle for base
    sketch.addGeometry(Part.LineSegment(
        App.Vector(-length/2, -width/2, 0),
        App.Vector(length/2, -width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(length/2, -width/2, 0),
        App.Vector(length/2, width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(length/2, width/2, 0),
        App.Vector(-length/2, width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(-length/2, width/2, 0),
        App.Vector(-length/2, -width/2, 0)
    ), False)
    
    doc.recompute()
    
    # Extrude base
    pad = base.newObject("PartDesign::Pad", "BasePad")
    pad.Profile = sketch
    pad.Length = DESIGN_PARAMETERS['base_height']
    
    doc.recompute()
    return base

def create_motor_housing():
    """Create the aluminum housing for the motor stator"""
    doc = App.ActiveDocument
    
    # Create housing body
    housing = doc.addObject("PartDesign::Body", "MotorHousing")
    
    # Create housing sketch
    sketch = housing.newObject("Sketcher::SketchObject", "HousingSketch")
    sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), 90))
    
    # Outer diameter
    outer_radius = DESIGN_PARAMETERS['housing_outer_diameter'] / 2
    sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), outer_radius), False)
    
    # Inner bore for stator
    inner_radius = DESIGN_PARAMETERS['housing_bore_diameter'] / 2
    sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), inner_radius), False)
    
    doc.recompute()
    
    # Extrude housing
    pad = housing.newObject("PartDesign::Pad", "HousingPad")
    pad.Profile = sketch
    pad.Length = DESIGN_PARAMETERS['housing_length']
    
    doc.recompute()
    
    # Add cooling fins if specified
    if DESIGN_PARAMETERS['housing_cooling_fins']:
        add_cooling_fins(housing)
    
    return housing

def add_cooling_fins(housing):
    """Add cooling fins to the motor housing"""
    doc = App.ActiveDocument
    
    fin_count = DESIGN_PARAMETERS['housing_fin_count']
    fin_height = DESIGN_PARAMETERS['housing_fin_height']
    housing_radius = DESIGN_PARAMETERS['housing_outer_diameter'] / 2
    
    for i in range(fin_count):
        angle = i * 360.0 / fin_count
        
        # Create fin sketch
        fin_sketch = housing.newObject("Sketcher::SketchObject", f"FinSketch_{i}")
        fin_sketch.Placement = App.Placement(
            App.Vector(0, 0, 0), 
            App.Rotation(App.Vector(0,0,1), angle)
        )
        
        # Define fin geometry (simple rectangular fin)
        fin_width = 5.0  # mm
        fin_sketch.addGeometry(Part.LineSegment(
            App.Vector(housing_radius, -fin_width/2, 0),
            App.Vector(housing_radius + fin_height, -fin_width/2, 0)
        ), False)
        fin_sketch.addGeometry(Part.LineSegment(
            App.Vector(housing_radius + fin_height, -fin_width/2, 0),
            App.Vector(housing_radius + fin_height, fin_width/2, 0)
        ), False)
        fin_sketch.addGeometry(Part.LineSegment(
            App.Vector(housing_radius + fin_height, fin_width/2, 0),
            App.Vector(housing_radius, fin_width/2, 0)
        ), False)
        fin_sketch.addGeometry(Part.LineSegment(
            App.Vector(housing_radius, fin_width/2, 0),
            App.Vector(housing_radius, -fin_width/2, 0)
        ), False)
        
        doc.recompute()
        
        # Extrude fin
        fin_pad = housing.newObject("PartDesign::Pad", f"FinPad_{i}")
        fin_pad.Profile = fin_sketch
        fin_pad.Length = DESIGN_PARAMETERS['housing_length']
        
    doc.recompute()

def create_shaft_assembly():
    """Create the precision shaft system"""
    doc = App.ActiveDocument
    
    # Create shaft body
    shaft = doc.addObject("PartDesign::Body", "MainShaft")
    
    # Create shaft sketch
    sketch = shaft.newObject("Sketcher::SketchObject", "ShaftSketch")
    sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(1,0,0), 90))
    
    # Shaft geometry
    radius = DESIGN_PARAMETERS['shaft_diameter'] / 2
    sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), radius), False)
    
    doc.recompute()
    
    # Extrude shaft
    pad = shaft.newObject("PartDesign::Pad", "ShaftPad")
    pad.Profile = sketch
    pad.Length = DESIGN_PARAMETERS['shaft_length']
    
    doc.recompute()
    
    # Add bearing locations
    add_bearing_seats(shaft)
    
    return shaft

def add_bearing_seats(shaft):
    """Add bearing seats to the shaft"""
    doc = App.ActiveDocument
    
    bearing_locations = [100, 300]  # mm from shaft start
    bearing_width = DESIGN_PARAMETERS['bearing_width']
    bearing_bore = DESIGN_PARAMETERS['bearing_bore']
    
    for i, location in enumerate(bearing_locations):
        # Create bearing seat sketch
        seat_sketch = shaft.newObject("Sketcher::SketchObject", f"BearingSeat_{i}")
        seat_sketch.Placement = App.Placement(
            App.Vector(0, 0, location), 
            App.Rotation(App.Vector(1,0,0), 90)
        )
        
        # Bearing seat geometry (slightly larger for fit)
        seat_radius = bearing_bore / 2 + 0.1  # mm clearance
        seat_sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), seat_radius), False)
        
        doc.recompute()

def create_sensor_mount():
    """Create the torque sensor mounting assembly"""
    doc = App.ActiveDocument
    
    # Create sensor mount body
    mount = doc.addObject("PartDesign::Body", "SensorMount")
    
    # Create mounting plate sketch
    sketch = mount.newObject("Sketcher::SketchObject", "MountSketch")
    sketch.Placement = App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1), 0))
    
    # Mount plate geometry (rectangular base)
    plate_length = 200.0  # mm
    plate_width = 150.0   # mm
    
    sketch.addGeometry(Part.LineSegment(
        App.Vector(-plate_length/2, -plate_width/2, 0),
        App.Vector(plate_length/2, -plate_width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(plate_length/2, -plate_width/2, 0),
        App.Vector(plate_length/2, plate_width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(plate_length/2, plate_width/2, 0),
        App.Vector(-plate_length/2, plate_width/2, 0)
    ), False)
    sketch.addGeometry(Part.LineSegment(
        App.Vector(-plate_length/2, plate_width/2, 0),
        App.Vector(-plate_length/2, -plate_width/2, 0)
    ), False)
    
    doc.recompute()
    
    # Extrude mount plate
    pad = mount.newObject("PartDesign::Pad", "MountPad")
    pad.Profile = sketch
    pad.Length = 25.0  # mm thickness
    
    doc.recompute()
    return mount

def generate_test_bed_assembly():
    """Generate the complete test bed assembly"""
    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument("MotorTestBed")
    
    print("Generating Motor Test Bed Assembly...")
    print(f"Motor: {DESIGN_PARAMETERS['motor_stator_diameter']}mm x {DESIGN_PARAMETERS['motor_stator_length']}mm")
    print(f"Torque Range: 0-{DESIGN_PARAMETERS['sensor_range']} Nm")
    print(f"Base Size: {DESIGN_PARAMETERS['base_length']}x{DESIGN_PARAMETERS['base_width']}x{DESIGN_PARAMETERS['base_height']} mm")
    
    # Create main components
    base_frame = create_base_frame()
    motor_housing = create_motor_housing()
    shaft_assembly = create_shaft_assembly()
    sensor_mount = create_sensor_mount()
    
    # Position components in assembly
    position_components(base_frame, motor_housing, shaft_assembly, sensor_mount)
    
    # Create assembly constraints
    create_assembly_constraints()
    
    doc.recompute()
    print("Test bed assembly generation complete!")
    
    return doc

def position_components(base, housing, shaft, sensor_mount):
    """Position all components in the assembly"""
    # Position motor housing on base
    housing.Placement = App.Placement(
        App.Vector(0, 0, DESIGN_PARAMETERS['base_height']), 
        App.Rotation(App.Vector(0,0,1), 0)
    )
    
    # Position shaft through housing
    shaft.Placement = App.Placement(
        App.Vector(0, 0, DESIGN_PARAMETERS['base_height'] - DESIGN_PARAMETERS['shaft_length']/4), 
        App.Rotation(App.Vector(0,0,1), 0)
    )
    
    # Position sensor mount
    sensor_mount.Placement = App.Placement(
        App.Vector(150, 0, DESIGN_PARAMETERS['base_height']), 
        App.Rotation(App.Vector(0,0,1), 0)
    )

def create_assembly_constraints():
    """Create parametric constraints between components"""
    # This would typically use FreeCAD's Assembly workbench
    # For now, we'll document the constraint requirements
    constraints = {
        'shaft_concentricity': f"±{DESIGN_PARAMETERS['alignment_tolerance']}mm TIR",
        'housing_fit': f"{DESIGN_PARAMETERS['housing_bore_tolerance']} tolerance",
        'bearing_preload': "10-20N axial force",
        'sensor_alignment': f"±{DESIGN_PARAMETERS['alignment_tolerance']}mm angular",
    }
    
    print("Assembly Constraints:")
    for constraint, value in constraints.items():
        print(f"  {constraint}: {value}")

def generate_parameter_report():
    """Generate a report of all design parameters"""
    print("\n" + "="*60)
    print("FREECAD PARAMETRIC DESIGN PARAMETERS")
    print("="*60)
    
    categories = {
        'Base Frame': ['base_length', 'base_width', 'base_height', 'base_material'],
        'Motor Specs': ['motor_stator_diameter', 'motor_stator_length', 'motor_rated_torque', 'motor_peak_torque'],
        'Housing': ['housing_outer_diameter', 'housing_length', 'housing_material'],
        'Shaft System': ['shaft_diameter', 'shaft_length', 'shaft_material'],
        'Torque Sensor': ['sensor_model', 'sensor_range', 'sensor_accuracy'],
        'Tolerances': ['alignment_tolerance', 'parallelism_tolerance', 'position_repeatability']
    }
    
    for category, params in categories.items():
        print(f"\n{category}:")
        for param in params:
            if param in DESIGN_PARAMETERS:
                print(f"  {param}: {DESIGN_PARAMETERS[param]}")
    
    print("="*60)

if __name__ == "__main__":
    # Generate parameter report
    generate_parameter_report()
    
    # Generate assembly (uncomment to run in FreeCAD)
    # generate_test_bed_assembly()