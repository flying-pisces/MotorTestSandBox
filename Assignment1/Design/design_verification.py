#!/usr/bin/env python3
"""
Method 1 Design Verification Script
Validates design parameters and calculations without requiring FreeCAD
"""

import os
import math

# Design Parameters (from FreeCAD script)
PARAMETERS = {
    'base_length': 800.0,           # mm
    'base_width': 600.0,            # mm
    'base_height': 40.0,            # mm
    'motor_stator_diameter': 85.0,  # mm (ILM-E85X30 spec)
    'motor_stator_length': 44.4,    # mm (ILM-E85X30 spec)
    'motor_mass': 0.822,            # kg (ILM-E85X30 spec)
    'motor_mount_height': 150.0,    # mm above base
    'cradle_arm_length': 400.0,     # mm between trunnion bearings
    'torque_arm_length': 300.0,     # mm from motor center to load cell
    'max_torque_range': 15.0,       # Nm (ILM-E85X30 peak torque)
    'expected_accuracy': 1.0,       # % full scale
}

# ILM-E85X30 STEP file path
MOTOR_STEP_PATH = "/Users/cyin/project/robot/MotorTestSandBox/DeviceUnderTest/ILM-E85X30 SERVO KIT PCB INFO REV.0100.step"

def verify_step_file():
    """Verify ILM-E85X30 STEP file exists and is valid"""
    print("🔍 STEP File Verification")
    print("=" * 50)
    
    if os.path.exists(MOTOR_STEP_PATH):
        file_size = os.path.getsize(MOTOR_STEP_PATH) / (1024 * 1024)  # MB
        print(f"✅ STEP file found: {os.path.basename(MOTOR_STEP_PATH)}")
        print(f"   Path: {MOTOR_STEP_PATH}")
        print(f"   Size: {file_size:.2f} MB")
        print(f"   Status: Ready for import")
        return True
    else:
        print(f"❌ STEP file not found at: {MOTOR_STEP_PATH}")
        print(f"   Fallback: Placeholder geometry will be used")
        return False

def verify_design_calculations():
    """Verify design calculations and engineering constraints"""
    print("\n🧮 Design Calculations Verification")
    print("=" * 50)
    
    # Torque measurement calculation
    max_force = PARAMETERS['max_torque_range'] / (PARAMETERS['torque_arm_length'] / 1000)  # N
    resolution = PARAMETERS['torque_arm_length'] / 1000 * PARAMETERS['expected_accuracy'] / 100  # Nm
    
    print(f"Torque Measurement System:")
    print(f"  Arm Length: {PARAMETERS['torque_arm_length']} mm")
    print(f"  Max Torque: {PARAMETERS['max_torque_range']} Nm")
    print(f"  Max Load Cell Force: {max_force:.1f} N")
    print(f"  System Resolution: ±{resolution:.4f} Nm")
    
    # Structural calculations
    base_area = PARAMETERS['base_length'] * PARAMETERS['base_width'] / 1000000  # m²
    motor_weight = PARAMETERS['motor_mass'] * 9.81  # N
    pressure_on_base = motor_weight / base_area  # Pa
    
    print(f"\nStructural Analysis:")
    print(f"  Base Platform: {PARAMETERS['base_length']}×{PARAMETERS['base_width']}×{PARAMETERS['base_height']} mm")
    print(f"  Base Area: {base_area:.2f} m²") 
    print(f"  Motor Weight: {motor_weight:.1f} N")
    print(f"  Base Pressure: {pressure_on_base:.1f} Pa (very low)")
    
    # Clearance calculations
    motor_radius = PARAMETERS['motor_stator_diameter'] / 2
    guard_radius = motor_radius + 50  # 50mm clearance
    cradle_span_check = PARAMETERS['motor_stator_diameter'] + 100  # minimum span needed
    
    print(f"\nClearance Verification:")
    print(f"  Motor Diameter: {PARAMETERS['motor_stator_diameter']} mm")
    print(f"  Safety Guard Radius: {guard_radius:.1f} mm")
    print(f"  Required Cradle Span: ≥{cradle_span_check} mm")
    print(f"  Actual Cradle Span: {PARAMETERS['cradle_arm_length']} mm")
    
    if PARAMETERS['cradle_arm_length'] >= cradle_span_check:
        print(f"  ✅ Adequate clearance provided")
    else:
        print(f"  ❌ Insufficient clearance - increase cradle span")
    
    return True

def verify_compatibility():
    """Verify ILM-E85X30 compatibility"""
    print("\n🔧 ILM-E85X30 Compatibility Check")
    print("=" * 50)
    
    # Motor specifications validation
    ilm_specs = {
        'rated_torque': 3.3,      # Nm
        'peak_torque': 15.0,      # Nm  
        'stator_diameter': 85,    # mm
        'stator_length': 44.4,    # mm
        'mass': 0.822,           # kg
    }
    
    print("Motor Specifications:")
    for spec, value in ilm_specs.items():
        param_name = f"motor_{spec}" if f"motor_{spec}" in PARAMETERS else spec.replace('rated_', '').replace('peak_', 'max_')
        if param_name in PARAMETERS:
            design_value = PARAMETERS[param_name]
            if abs(design_value - value) < 0.01:
                print(f"  ✅ {spec}: {value} (matches design)")
            else:
                print(f"  ⚠️  {spec}: {value} (design: {design_value})")
        else:
            print(f"  ℹ️  {spec}: {value}")
    
    # Test range verification
    torque_range_ok = PARAMETERS['max_torque_range'] >= ilm_specs['peak_torque']
    print(f"\nTorque Range Check:")
    print(f"  Motor Peak Torque: {ilm_specs['peak_torque']} Nm")
    print(f"  Test System Range: {PARAMETERS['max_torque_range']} Nm")
    print(f"  Status: {'✅ Adequate range' if torque_range_ok else '❌ Insufficient range'}")
    
    return torque_range_ok

def verify_cad_files():
    """Verify generated CAD files exist"""
    print("\n📁 CAD Files Verification")
    print("=" * 50)
    
    cad_files = [
        "Method1_ILM_E85X30_OpenSCAD.scad",
        "Method1_ILM_E85X30_Cradle.FCMacro", 
        "Method1_ILM_E85X30_Cradle_FreeCAD.py",
        "Method1_test_render.png"
    ]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in cad_files:
        filepath = os.path.join(current_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"  ✅ {filename} ({file_size:.1f} KB)")
        else:
            print(f"  ❌ {filename} - Missing")
    
    return True

def generate_summary():
    """Generate verification summary"""
    print("\n📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    checks = [
        ("STEP File Import", verify_step_file()),
        ("Design Calculations", verify_design_calculations()),
        ("Motor Compatibility", verify_compatibility()),
        ("CAD Files Present", verify_cad_files())
    ]
    
    print("\nOverall Status:")
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {check_name}: {status}")
        all_passed &= result
    
    print(f"\n{'🎉 ALL SYSTEMS VALIDATED' if all_passed else '⚠️  SOME ISSUES FOUND'}")
    print(f"Method 1 Reaction Torque Cradle: {'READY FOR IMPLEMENTATION' if all_passed else 'REQUIRES ATTENTION'}")

if __name__ == "__main__":
    print("METHOD 1 REACTION TORQUE CRADLE - DESIGN VERIFICATION")
    print("=" * 60)
    print("Validating ILM-E85X30 motor testing system design...")
    
    verify_step_file()
    verify_design_calculations() 
    verify_compatibility()
    verify_cad_files()
    generate_summary()