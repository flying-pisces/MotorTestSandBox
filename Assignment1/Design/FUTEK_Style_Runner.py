#!/usr/bin/env python3
"""
FUTEK-Style Test Bench - Standalone Runner
Generates both OpenSCAD and FreeCAD models following Example 2 reference design
"""

import os
from FUTEK_Style_Parameters import generate_futek_style_report, FUTEK_PARAMETERS

def create_futek_freecad_macro():
    """Create FreeCAD macro for FUTEK-style test bench"""
    
    macro_content = '''# FreeCAD Macro: FUTEK-Style Horizontal Motor Test Bench
# Professional Configuration: Motor → Torque Sensor → Eddy Current Brake
# Based on Example 2 reference design

import FreeCAD as App
import Part

# Design Parameters
FUTEK_PARAMETERS = ''' + str(FUTEK_PARAMETERS) + '''

def create_base_platform():
    """Create aluminum base platform"""
    doc = App.ActiveDocument
    
    base = doc.addObject("Part::Box", "BasePlatform")
    base.Length = FUTEK_PARAMETERS['base_length']
    base.Width = FUTEK_PARAMETERS['base_width'] 
    base.Height = FUTEK_PARAMETERS['base_height']
    base.Placement = App.Placement(
        App.Vector(0, -FUTEK_PARAMETERS['base_width']/2, 0),
        App.Rotation(0, 0, 0, 1)
    )
    
    return base

def create_motor_assembly():
    """Create motor assembly at left position"""
    doc = App.ActiveDocument
    
    # Motor housing (ILM-E85x30)
    motor = doc.addObject("Part::Cylinder", "MotorHousing")
    motor.Radius = FUTEK_PARAMETERS['motor_stator_diameter'] / 2
    motor.Height = FUTEK_PARAMETERS['motor_stator_length']
    motor.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['motor_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    return motor

def create_torque_sensor():
    """Create FUTEK TRS-style torque sensor"""
    doc = App.ActiveDocument
    
    # Sensor body (red - FUTEK style)
    sensor = doc.addObject("Part::Cylinder", "TorqueSensor")
    sensor.Radius = FUTEK_PARAMETERS['sensor_diameter'] / 2
    sensor.Height = FUTEK_PARAMETERS['sensor_length']
    sensor.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['sensor_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    return sensor

def create_brake_assembly():
    """Create eddy current brake with finned disc"""
    doc = App.ActiveDocument
    
    # Brake housing
    brake_housing = doc.addObject("Part::Box", "BrakeHousing")
    brake_housing.Length = FUTEK_PARAMETERS['brake_housing_width']
    brake_housing.Width = FUTEK_PARAMETERS['brake_housing_width']
    brake_housing.Height = FUTEK_PARAMETERS['brake_housing_height']
    brake_housing.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['brake_position_x'] - FUTEK_PARAMETERS['brake_housing_width']/2,
                  -FUTEK_PARAMETERS['brake_housing_width']/2,
                  FUTEK_PARAMETERS['motor_mount_height'] - 40),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Brake disc with fins
    brake_disc = doc.addObject("Part::Cylinder", "BrakeDisc")
    brake_disc.Radius = FUTEK_PARAMETERS['brake_disc_diameter'] / 2
    brake_disc.Height = FUTEK_PARAMETERS['brake_disc_thickness']
    brake_disc.Placement = App.Placement(
        App.Vector(FUTEK_PARAMETERS['brake_position_x'], 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    return [brake_housing, brake_disc]

def create_main_shaft():
    """Create the main shaft connecting motor to brake"""
    doc = App.ActiveDocument
    
    shaft_start_x = FUTEK_PARAMETERS['motor_position_x'] + 100  # Approximate
    shaft_length = FUTEK_PARAMETERS['brake_position_x'] - shaft_start_x - 100
    
    shaft = doc.addObject("Part::Cylinder", "MainShaft")
    shaft.Radius = FUTEK_PARAMETERS['main_shaft_diameter'] / 2
    shaft.Height = shaft_length
    shaft.Placement = App.Placement(
        App.Vector(shaft_start_x, 0, FUTEK_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(0,1,0), 90)
    )
    
    return shaft

def create_bearing_pedestals():
    """Create bearing pedestals"""
    doc = App.ActiveDocument
    
    pedestals = []
    positions = [
        FUTEK_PARAMETERS['motor_position_x'],
        FUTEK_PARAMETERS['sensor_position_x'] - 60,
        FUTEK_PARAMETERS['sensor_position_x'] + 60,
        FUTEK_PARAMETERS['brake_position_x']
    ]
    
    for i, pos_x in enumerate(positions):
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
        pedestals.append(pedestal)
    
    return pedestals

def apply_colors(components):
    """Apply professional colors to components"""
    color_scheme = {
        'BasePlatform': (0.7, 0.7, 0.7),        # Aluminum gray
        'MotorHousing': (0.2, 0.3, 0.8),        # Blue motor
        'TorqueSensor': (0.8, 0.1, 0.1),        # FUTEK red
        'BrakeHousing': (0.3, 0.3, 0.3),        # Dark gray
        'BrakeDisc': (0.3, 0.3, 0.3),           # Dark gray
        'MainShaft': (0.9, 0.9, 0.8),           # Stainless steel
    }
    
    for obj in App.ActiveDocument.Objects:
        if obj.Name.startswith('Pedestal'):
            obj.ViewObject.ShapeColor = (0.8, 0.8, 0.9)  # Light aluminum
        elif obj.Name in color_scheme:
            obj.ViewObject.ShapeColor = color_scheme[obj.Name]

def generate_futek_assembly():
    """Generate complete FUTEK-style assembly"""
    # Create new document
    doc = App.newDocument("FUTEK_MotorTestBench")
    
    print("Creating FUTEK-Style Horizontal Motor Test Bench...")
    
    # Create all components
    base = create_base_platform()
    motor = create_motor_assembly()
    sensor = create_torque_sensor()
    brake_parts = create_brake_assembly()
    shaft = create_main_shaft()
    pedestals = create_bearing_pedestals()
    
    # Apply colors
    apply_colors([base, motor, sensor] + brake_parts + [shaft] + pedestals)
    
    doc.recompute()
    
    # Fit view
    try:
        App.Gui.SendMsgToActiveView("ViewFit")
    except:
        pass
    
    print("Assembly Complete!")
    print(f"Total Length: {FUTEK_PARAMETERS['base_length']} mm")
    print(f"Motor Position: {FUTEK_PARAMETERS['motor_position_x']} mm")
    print(f"Sensor Position: {FUTEK_PARAMETERS['sensor_position_x']} mm")
    print(f"Brake Position: {FUTEK_PARAMETERS['brake_position_x']} mm")
    
    return doc

# Execute the assembly
if __name__ == "__main__":
    generate_futek_assembly()
'''
    
    with open('FUTEK_Style_FreeCAD_Macro.FCMacro', 'w') as f:
        f.write(macro_content)
    
    return 'FUTEK_Style_FreeCAD_Macro.FCMacro'

def compare_designs():
    """Compare original vs FUTEK-style designs"""
    print("\n" + "="*70)
    print("DESIGN COMPARISON: Original vs FUTEK-Style")
    print("="*70)
    
    comparison_table = [
        ["Feature", "Original Design", "FUTEK-Style"],
        ["Orientation", "Vertical mount", "Horizontal shaft"],
        ["Configuration", "Motor above base", "Motor → Sensor → Brake"],
        ["Base Size", "800×600×150mm", "1000×400×20mm"],
        ["Torque Sensor", "HBK T210-10Nm", "FUTEK TRS-50Nm"],
        ["Sensor Position", "Beside motor", "Between motor & brake"],
        ["Load Device", "Hysteresis brake", "Eddy current brake"],
        ["Shaft System", "50mm vertical", "25mm horizontal"],
        ["Bearing Mounts", "Integrated housing", "Professional pedestals"],
        ["Industry Standard", "Academic approach", "Commercial standard"],
        ["Maintenance", "Limited access", "Easy access"],
        ["Expansion", "Difficult", "Modular design"],
    ]
    
    for row in comparison_table:
        print(f"{row[0]:<20} | {row[1]:<20} | {row[2]:<20}")
    
    print("="*70)
    print("RECOMMENDATION: FUTEK-Style follows industry best practices")
    print("- Horizontal configuration is standard for motor testing")
    print("- Sensor between motor and load provides direct measurement")
    print("- Professional bearing pedestals enable easy maintenance")
    print("- Modular design allows component upgrades")
    print("="*70)

def main():
    """Main execution function"""
    print("🎯 FUTEK-STYLE MOTOR TEST BENCH GENERATOR")
    print("Following Example 2 Professional Design\n")
    
    # Generate parameter report
    generate_futek_style_report()
    
    # Create FreeCAD macro
    macro_file = create_futek_freecad_macro()
    print(f"\n✅ FreeCAD Macro Generated: {macro_file}")
    
    # Compare designs
    compare_designs()
    
    print(f"\n🚀 FUTEK-STYLE DESIGN COMPLETE!")
    print(f"Files Generated:")
    print(f"  - OpenSCAD Model: FUTEK_Style_OpenSCAD.scad")
    print(f"  - FreeCAD Macro: {macro_file}")
    print(f"  - Rendered Preview: FUTEK_Style_Preview.png")
    print(f"\nTo use:")
    print(f"  1. OpenSCAD: Load .scad file and render")
    print(f"  2. FreeCAD: Run macro from Macro menu")
    print(f"  3. Both models follow professional industry standards")

if __name__ == "__main__":
    main()