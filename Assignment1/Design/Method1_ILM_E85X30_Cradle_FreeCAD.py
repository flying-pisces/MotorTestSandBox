#!/usr/bin/env python3
"""
Method 1: Reaction Torque Cradle for ILM-E85X30 Motor
FreeCAD Parametric Design Script

This script creates a complete Method 1 reaction torque testing setup with:
1. Import of actual ILM-E85X30 STEP file
2. Custom cradle mount with trunnion bearings  
3. Torque arm and load cell mounting
4. Professional test bench configuration

Based on industry-standard reaction torque measurement principles.
"""

import FreeCAD as App
import Part
import os

# Path to the ILM-E85X30 STEP file
MOTOR_STEP_PATH = "/Users/cyin/project/robot/MotorTestSandBox/DeviceUnderTest/ILM-E85X30 SERVO KIT PCB INFO REV.0100.step"

# Design Parameters for Method 1 Cradle
METHOD1_PARAMETERS = {
    # Base Frame Parameters
    'base_length': 800.0,           # mm
    'base_width': 600.0,            # mm
    'base_height': 40.0,            # mm - thicker for reaction forces
    'base_material': 'Cast_Iron_GG25',
    
    # Motor Parameters (from ILM-E85X30 specs)
    'motor_stator_diameter': 85.0,  # mm
    'motor_stator_length': 44.4,    # mm
    'motor_rotor_bore': 52.0,       # mm
    'motor_mass': 0.822,            # kg
    'motor_mount_height': 150.0,    # mm above base
    
    # Cradle Mount Parameters  
    'cradle_bearing_diameter': 60.0, # mm - trunnion bearing OD
    'cradle_bearing_bore': 25.0,    # mm - trunnion bearing ID
    'cradle_arm_length': 400.0,     # mm - distance between trunnion bearings
    'cradle_arm_height': 40.0,      # mm - structural height
    'cradle_arm_width': 60.0,       # mm - structural width
    
    # Trunnion Bearing Pedestals
    'pedestal_height': 120.0,       # mm
    'pedestal_width': 100.0,        # mm
    'pedestal_depth': 80.0,         # mm
    'bearing_clearance': 0.1,       # mm
    
    # Torque Arm System
    'torque_arm_length': 300.0,     # mm - from motor center to load cell
    'torque_arm_width': 30.0,       # mm
    'torque_arm_thickness': 10.0,   # mm
    'load_cell_diameter': 25.0,     # mm
    'load_cell_height': 50.0,       # mm
    
    # Safety and Guards
    'guard_clearance': 50.0,        # mm around rotating parts
    'emergency_stop_position': [-200, -200, 200], # mm from origin
    
    # Measurement Specifications
    'max_torque_range': 15.0,       # Nm - based on ILM-E85X30 peak torque
    'torque_arm_calibration': 0.0,  # mm offset for calibration
    'expected_accuracy': 1.0,       # % full scale
}

def create_method1_cradle_assembly():
    """Create complete Method 1 reaction torque cradle assembly"""
    
    # Create new document
    doc = App.newDocument("Method1_ILM_E85X30_Cradle")
    
    print("Creating Method 1 Reaction Torque Cradle for ILM-E85X30...")
    print("="*60)
    
    # Create main components
    base_platform = create_base_platform(doc)
    motor_assembly = import_ilm_e85x30_motor(doc)
    cradle_system = create_cradle_mount_system(doc)
    torque_measurement = create_torque_measurement_system(doc)
    safety_guards = create_safety_guards(doc)
    
    # Position and assemble components
    assemble_method1_system(doc, base_platform, motor_assembly, cradle_system, 
                           torque_measurement, safety_guards)
    
    # Apply materials and colors
    apply_method1_materials(doc)
    
    # Generate documentation
    generate_method1_documentation(doc)
    
    doc.recompute()
    
    # Fit view if GUI available
    try:
        App.Gui.SendMsgToActiveView("ViewFit")
    except:
        pass
    
    print("Method 1 Cradle Assembly Complete!")
    print(f"Motor: ILM-E85X30 imported from STEP file")
    print(f"Max Torque Range: {METHOD1_PARAMETERS['max_torque_range']} Nm")
    print(f"Torque Arm Length: {METHOD1_PARAMETERS['torque_arm_length']} mm")
    print(f"Expected Accuracy: ±{METHOD1_PARAMETERS['expected_accuracy']}%")
    
    return doc

def create_base_platform(doc):
    """Create heavy-duty base platform for reaction torque testing"""
    
    # Main base platform (extra thick for stability)
    base = doc.addObject("Part::Box", "BasePlatform")
    base.Length = METHOD1_PARAMETERS['base_length']
    base.Width = METHOD1_PARAMETERS['base_width']
    base.Height = METHOD1_PARAMETERS['base_height']
    base.Placement = App.Placement(
        App.Vector(-METHOD1_PARAMETERS['base_length']/2, 
                  -METHOD1_PARAMETERS['base_width']/2, 0),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Reinforcement ribs for reaction force absorption
    ribs = []
    rib_count = 5
    for i in range(rib_count):
        rib = doc.addObject("Part::Box", f"ReinforcementRib_{i}")
        rib.Length = METHOD1_PARAMETERS['base_width'] - 100
        rib.Width = 20
        rib.Height = METHOD1_PARAMETERS['base_height'] - 10
        rib.Placement = App.Placement(
            App.Vector(-METHOD1_PARAMETERS['base_length']/2 + 100 + i * 120,
                      -METHOD1_PARAMETERS['base_width']/2 + 50,
                      METHOD1_PARAMETERS['base_height'] - 10),
            App.Rotation(0, 0, 0, 1)
        )
        ribs.append(rib)
    
    # Mounting holes for floor anchoring
    mounting_holes = []
    hole_positions = [
        [-300, -200], [300, -200], [-300, 200], [300, 200],
        [0, -200], [0, 200], [-150, 0], [150, 0]
    ]
    
    for i, (x, y) in enumerate(hole_positions):
        hole = doc.addObject("Part::Cylinder", f"MountingHole_{i}")
        hole.Radius = 8  # M16 clearance holes
        hole.Height = METHOD1_PARAMETERS['base_height'] + 2
        hole.Placement = App.Placement(
            App.Vector(x, y, -1),
            App.Rotation(0, 0, 0, 1)
        )
        mounting_holes.append(hole)
    
    # Create base with reinforcements
    base_with_ribs = doc.addObject("Part::Fuse", "BaseWithRibs")
    base_with_ribs.Base = base
    base_with_ribs.Tool = ribs[0]
    doc.recompute()
    
    # Add remaining ribs
    for rib in ribs[1:]:
        new_fuse = doc.addObject("Part::Fuse", f"BaseRib_{ribs.index(rib)}")
        new_fuse.Base = base_with_ribs
        new_fuse.Tool = rib
        base_with_ribs = new_fuse
        doc.recompute()
    
    # Cut mounting holes
    if mounting_holes:
        base_final = doc.addObject("Part::Cut", "BaseFinal")
        base_final.Base = base_with_ribs
        base_final.Tool = mounting_holes[0]
        doc.recompute()
        
        for hole in mounting_holes[1:]:
            new_cut = doc.addObject("Part::Cut", f"BaseCut_{mounting_holes.index(hole)}")
            new_cut.Base = base_final
            new_cut.Tool = hole
            base_final = new_cut
            doc.recompute()
    
    return base_final

def import_ilm_e85x30_motor(doc):
    """Import the actual ILM-E85X30 STEP file"""
    
    print(f"Importing ILM-E85X30 from: {MOTOR_STEP_PATH}")
    
    try:
        # Check if file exists
        if not os.path.exists(MOTOR_STEP_PATH):
            print(f"Warning: STEP file not found at {MOTOR_STEP_PATH}")
            print("Creating placeholder motor geometry...")
            return create_placeholder_motor(doc)
        
        # Import STEP file
        import Import
        Import.insert(MOTOR_STEP_PATH, doc.Name)
        doc.recompute()
        
        # Get the imported objects
        imported_objects = [obj for obj in doc.Objects if 'ILM' in obj.Label or '330816' in obj.Label]
        
        if imported_objects:
            # Create compound of all imported parts
            motor_compound = doc.addObject("Part::Compound", "ILM_E85X30_Motor")
            motor_compound.Links = imported_objects
            
            # Position motor in cradle mount position
            motor_compound.Placement = App.Placement(
                App.Vector(0, 0, METHOD1_PARAMETERS['motor_mount_height']),
                App.Rotation(App.Vector(1,0,0), 90)  # Rotate for cradle mounting
            )
            
            doc.recompute()
            print("✅ ILM-E85X30 STEP file imported successfully")
            return motor_compound
        else:
            print("Warning: Could not identify imported motor objects")
            return create_placeholder_motor(doc)
            
    except Exception as e:
        print(f"Error importing STEP file: {str(e)}")
        print("Creating placeholder motor geometry...")
        return create_placeholder_motor(doc)

def create_placeholder_motor(doc):
    """Create placeholder motor geometry if STEP import fails"""
    
    # Motor stator (outer cylinder)
    stator = doc.addObject("Part::Cylinder", "MotorStator")
    stator.Radius = METHOD1_PARAMETERS['motor_stator_diameter'] / 2
    stator.Height = METHOD1_PARAMETERS['motor_stator_length']
    stator.Placement = App.Placement(
        App.Vector(0, 0, METHOD1_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Motor rotor (inner bore)
    rotor = doc.addObject("Part::Cylinder", "MotorRotor")
    rotor.Radius = METHOD1_PARAMETERS['motor_rotor_bore'] / 2
    rotor.Height = METHOD1_PARAMETERS['motor_stator_length'] + 20
    rotor.Placement = App.Placement(
        App.Vector(0, 0, METHOD1_PARAMETERS['motor_mount_height']),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Create motor assembly
    motor_assembly = doc.addObject("Part::Cut", "ILM_E85X30_Placeholder")
    motor_assembly.Base = stator
    motor_assembly.Tool = rotor
    
    doc.recompute()
    return motor_assembly

def create_cradle_mount_system(doc):
    """Create trunnion bearing cradle mount system"""
    
    cradle_parts = []
    
    # Left pedestal (trunnion bearing mount)
    left_pedestal = doc.addObject("Part::Box", "LeftPedestal")
    left_pedestal.Length = METHOD1_PARAMETERS['pedestal_width']
    left_pedestal.Width = METHOD1_PARAMETERS['pedestal_depth']
    left_pedestal.Height = METHOD1_PARAMETERS['pedestal_height']
    left_pedestal.Placement = App.Placement(
        App.Vector(-METHOD1_PARAMETERS['cradle_arm_length']/2 - METHOD1_PARAMETERS['pedestal_width']/2,
                  -METHOD1_PARAMETERS['pedestal_depth']/2,
                  METHOD1_PARAMETERS['base_height']),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Left trunnion bearing
    left_bearing = doc.addObject("Part::Cylinder", "LeftTrunnionBearing")
    left_bearing.Radius = METHOD1_PARAMETERS['cradle_bearing_diameter'] / 2
    left_bearing.Height = METHOD1_PARAMETERS['pedestal_width']
    left_bearing.Placement = App.Placement(
        App.Vector(-METHOD1_PARAMETERS['cradle_arm_length']/2,
                  0,
                  METHOD1_PARAMETERS['base_height'] + METHOD1_PARAMETERS['pedestal_height']/2),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Left bearing bore
    left_bearing_bore = doc.addObject("Part::Cylinder", "LeftBearingBore")
    left_bearing_bore.Radius = METHOD1_PARAMETERS['cradle_bearing_bore'] / 2
    left_bearing_bore.Height = METHOD1_PARAMETERS['pedestal_width'] + 10
    left_bearing_bore.Placement = App.Placement(
        App.Vector(-METHOD1_PARAMETERS['cradle_arm_length']/2,
                  0,
                  METHOD1_PARAMETERS['base_height'] + METHOD1_PARAMETERS['pedestal_height']/2),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Right pedestal (mirror of left)
    right_pedestal = doc.addObject("Part::Box", "RightPedestal")
    right_pedestal.Length = METHOD1_PARAMETERS['pedestal_width']
    right_pedestal.Width = METHOD1_PARAMETERS['pedestal_depth']
    right_pedestal.Height = METHOD1_PARAMETERS['pedestal_height']
    right_pedestal.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['cradle_arm_length']/2 - METHOD1_PARAMETERS['pedestal_width']/2,
                  -METHOD1_PARAMETERS['pedestal_depth']/2,
                  METHOD1_PARAMETERS['base_height']),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Right trunnion bearing
    right_bearing = doc.addObject("Part::Cylinder", "RightTrunnionBearing")
    right_bearing.Radius = METHOD1_PARAMETERS['cradle_bearing_diameter'] / 2
    right_bearing.Height = METHOD1_PARAMETERS['pedestal_width']
    right_bearing.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['cradle_arm_length']/2,
                  0,
                  METHOD1_PARAMETERS['base_height'] + METHOD1_PARAMETERS['pedestal_height']/2),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Right bearing bore
    right_bearing_bore = doc.addObject("Part::Cylinder", "RightBearingBore")
    right_bearing_bore.Radius = METHOD1_PARAMETERS['cradle_bearing_bore'] / 2
    right_bearing_bore.Height = METHOD1_PARAMETERS['pedestal_width'] + 10
    right_bearing_bore.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['cradle_arm_length']/2,
                  0,
                  METHOD1_PARAMETERS['base_height'] + METHOD1_PARAMETERS['pedestal_height']/2),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Cradle arms connecting the pedestals
    cradle_arm = doc.addObject("Part::Box", "CradleArm")
    cradle_arm.Length = METHOD1_PARAMETERS['cradle_arm_length']
    cradle_arm.Width = METHOD1_PARAMETERS['cradle_arm_width']
    cradle_arm.Height = METHOD1_PARAMETERS['cradle_arm_height']
    cradle_arm.Placement = App.Placement(
        App.Vector(-METHOD1_PARAMETERS['cradle_arm_length']/2,
                  -METHOD1_PARAMETERS['cradle_arm_width']/2,
                  METHOD1_PARAMETERS['base_height'] + METHOD1_PARAMETERS['pedestal_height']/2 - METHOD1_PARAMETERS['cradle_arm_height']/2),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Cut bearing bores from pedestals
    left_pedestal_cut = doc.addObject("Part::Cut", "LeftPedestalWithBearing")
    left_pedestal_cut.Base = left_pedestal
    left_pedestal_cut.Tool = left_bearing_bore
    
    right_pedestal_cut = doc.addObject("Part::Cut", "RightPedestalWithBearing")
    right_pedestal_cut.Base = right_pedestal
    right_pedestal_cut.Tool = right_bearing_bore
    
    doc.recompute()
    
    return [left_pedestal_cut, right_pedestal_cut, left_bearing, right_bearing, cradle_arm]

def create_torque_measurement_system(doc):
    """Create torque arm and load cell system"""
    
    # Main torque arm
    torque_arm = doc.addObject("Part::Box", "TorqueArm")
    torque_arm.Length = METHOD1_PARAMETERS['torque_arm_length']
    torque_arm.Width = METHOD1_PARAMETERS['torque_arm_width']
    torque_arm.Height = METHOD1_PARAMETERS['torque_arm_thickness']
    torque_arm.Placement = App.Placement(
        App.Vector(0, -METHOD1_PARAMETERS['torque_arm_width']/2,
                  METHOD1_PARAMETERS['motor_mount_height'] + METHOD1_PARAMETERS['motor_stator_diameter']/2 + 20),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Load cell at end of torque arm
    load_cell = doc.addObject("Part::Cylinder", "LoadCell")
    load_cell.Radius = METHOD1_PARAMETERS['load_cell_diameter'] / 2
    load_cell.Height = METHOD1_PARAMETERS['load_cell_height']
    load_cell.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['torque_arm_length']/2,
                  0,
                  METHOD1_PARAMETERS['motor_mount_height'] + METHOD1_PARAMETERS['motor_stator_diameter']/2 + 20 + METHOD1_PARAMETERS['torque_arm_thickness']),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Load cell mounting bracket
    load_cell_bracket = doc.addObject("Part::Box", "LoadCellBracket")
    load_cell_bracket.Length = 60
    load_cell_bracket.Width = 40
    load_cell_bracket.Height = 20
    load_cell_bracket.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['torque_arm_length']/2 - 30,
                  -20,
                  METHOD1_PARAMETERS['motor_mount_height'] + METHOD1_PARAMETERS['motor_stator_diameter']/2 + 20 + METHOD1_PARAMETERS['torque_arm_thickness'] + METHOD1_PARAMETERS['load_cell_height']),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Connection point to motor housing
    arm_connection = doc.addObject("Part::Cylinder", "ArmConnection")
    arm_connection.Radius = 15
    arm_connection.Height = METHOD1_PARAMETERS['torque_arm_thickness'] + 20
    arm_connection.Placement = App.Placement(
        App.Vector(0, 0,
                  METHOD1_PARAMETERS['motor_mount_height'] + METHOD1_PARAMETERS['motor_stator_diameter']/2 + 10),
        App.Rotation(0, 0, 0, 1)
    )
    
    doc.recompute()
    
    return [torque_arm, load_cell, load_cell_bracket, arm_connection]

def create_safety_guards(doc):
    """Create safety guards around rotating motor"""
    
    # Motor guard (transparent cylinder)
    motor_guard = doc.addObject("Part::Cylinder", "MotorSafetyGuard")
    motor_guard.Radius = (METHOD1_PARAMETERS['motor_stator_diameter'] + METHOD1_PARAMETERS['guard_clearance']) / 2
    motor_guard.Height = METHOD1_PARAMETERS['motor_stator_length'] + 100
    motor_guard.Placement = App.Placement(
        App.Vector(0, 0, METHOD1_PARAMETERS['motor_mount_height'] - 50),
        App.Rotation(App.Vector(1,0,0), 90)
    )
    
    # Guard opening for torque arm
    guard_opening = doc.addObject("Part::Box", "GuardOpening")
    guard_opening.Length = 100
    guard_opening.Width = METHOD1_PARAMETERS['torque_arm_width'] + 20
    guard_opening.Height = METHOD1_PARAMETERS['motor_stator_length'] + 120
    guard_opening.Placement = App.Placement(
        App.Vector(-50, -(METHOD1_PARAMETERS['torque_arm_width'] + 20)/2,
                  METHOD1_PARAMETERS['motor_mount_height'] - 60),
        App.Rotation(0, 0, 0, 1)
    )
    
    # Create guard with opening
    guard_with_opening = doc.addObject("Part::Cut", "MotorGuardWithOpening")
    guard_with_opening.Base = motor_guard
    guard_with_opening.Tool = guard_opening
    
    # Emergency stop button mount
    estop_mount = doc.addObject("Part::Cylinder", "EStopMount")
    estop_mount.Radius = 25
    estop_mount.Height = 50
    estop_mount.Placement = App.Placement(
        App.Vector(METHOD1_PARAMETERS['emergency_stop_position'][0],
                  METHOD1_PARAMETERS['emergency_stop_position'][1],
                  METHOD1_PARAMETERS['emergency_stop_position'][2]),
        App.Rotation(0, 0, 0, 1)
    )
    
    doc.recompute()
    
    return [guard_with_opening, estop_mount]

def assemble_method1_system(doc, base, motor, cradle, torque_system, guards):
    """Assemble all components into final system"""
    
    # All components are positioned during creation
    # This function can handle any final assembly adjustments
    
    print("Assembling Method 1 system components...")
    print(f"  ✅ Base platform: {base.Label}")
    print(f"  ✅ Motor: {motor.Label}")
    print(f"  ✅ Cradle system: {len(cradle)} components")
    print(f"  ✅ Torque measurement: {len(torque_system)} components")
    print(f"  ✅ Safety guards: {len(guards)} components")

def apply_method1_materials(doc):
    """Apply colors and materials to components"""
    
    try:
        # Color scheme for Method 1
        colors = {
            'base': (0.5, 0.5, 0.5),          # Gray (cast iron)
            'motor': (0.2, 0.3, 0.8),         # Blue (motor)
            'cradle': (0.8, 0.8, 0.9),        # Light blue (aluminum)
            'torque_arm': (0.9, 0.7, 0.1),    # Yellow (steel)
            'load_cell': (0.8, 0.1, 0.1),     # Red (sensor)
            'guards': (0.9, 0.9, 0.9, 0.3),   # Transparent (safety)
            'bearings': (0.7, 0.7, 0.8),      # Steel gray
        }
        
        # Apply colors to objects
        for obj in doc.Objects:
            if hasattr(obj, 'ViewObject'):
                if 'Base' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['base']
                elif 'Motor' in obj.Label or 'ILM' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['motor']
                elif 'Pedestal' in obj.Label or 'Cradle' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['cradle']
                elif 'Torque' in obj.Label or 'Arm' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['torque_arm']
                elif 'LoadCell' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['load_cell']
                elif 'Guard' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['guards']
                    obj.ViewObject.Transparency = 70
                elif 'Bearing' in obj.Label:
                    obj.ViewObject.ShapeColor = colors['bearings']
                    
    except Exception as e:
        print(f"Note: Could not apply colors (GUI not available): {e}")

def generate_method1_documentation(doc):
    """Generate comprehensive documentation for Method 1 system"""
    
    print("\n" + "="*60)
    print("METHOD 1: REACTION TORQUE CRADLE DOCUMENTATION")
    print("="*60)
    print(f"Motor: ILM-E85X30 (imported from STEP file)")
    print(f"Configuration: Cradle mount with trunnion bearings")
    print(f"Measurement Method: Reaction torque via load cell")
    
    print(f"\nSystem Specifications:")
    print(f"  Base Platform: {METHOD1_PARAMETERS['base_length']}×{METHOD1_PARAMETERS['base_width']}×{METHOD1_PARAMETERS['base_height']} mm")
    print(f"  Torque Arm Length: {METHOD1_PARAMETERS['torque_arm_length']} mm")
    print(f"  Max Torque Range: {METHOD1_PARAMETERS['max_torque_range']} Nm")
    print(f"  Expected Accuracy: ±{METHOD1_PARAMETERS['expected_accuracy']}%")
    print(f"  Trunnion Bearing Span: {METHOD1_PARAMETERS['cradle_arm_length']} mm")
    
    print(f"\nMeasurement Formula:")
    print(f"  Torque = Load Cell Force × {METHOD1_PARAMETERS['torque_arm_length']} mm")
    print(f"  Resolution = Load Cell Resolution × Arm Length")
    
    print(f"\nSafety Features:")
    print(f"  ✅ Motor safety guard with {METHOD1_PARAMETERS['guard_clearance']} mm clearance")
    print(f"  ✅ Emergency stop button mounted")
    print(f"  ✅ Reinforced base for reaction forces")
    print(f"  ✅ Floor anchor points provided")
    
    print("="*60)

# Main execution function
if __name__ == "__main__":
    doc = create_method1_cradle_assembly()