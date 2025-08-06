#!/usr/bin/env python3
"""
FUTEK-Style Horizontal Motor Test Bench Parameters
Based on Example 2 reference - Professional horizontal configuration
Motor → Torque Sensor → Eddy Current Brake

Key Design Features:
- Horizontal shaft configuration (industry standard)
- FUTEK TRS torque sensor between motor and brake
- Eddy current brake with finned disc
- Professional bearing pedestals
- Integrated data acquisition system
"""

# Master Design Parameters for FUTEK-Style Test Bench
FUTEK_PARAMETERS = {
    # Base Platform Parameters
    'base_length': 1000.0,          # mm - longer for horizontal layout
    'base_width': 400.0,            # mm - narrower than vertical design
    'base_height': 20.0,            # mm - aluminum plate thickness
    'base_material': 'Aluminum_6061_T6',
    'base_mounting_holes': 8,       # M8 mounting holes
    
    # Motor Mount (Left Side)
    'motor_position_x': 150.0,      # mm from left edge
    'motor_mount_height': 100.0,    # mm above base
    'motor_stator_diameter': 85.0,  # mm - ILM-E85x30
    'motor_stator_length': 44.4,    # mm
    'motor_rotor_bore': 52.0,       # mm
    'motor_shaft_extension': 50.0,  # mm beyond stator
    
    # Torque Sensor (Center)
    'sensor_position_x': 500.0,     # mm from left edge (center)
    'sensor_type': 'FUTEK_TRS600',  # Similar to reference
    'sensor_length': 100.0,         # mm
    'sensor_diameter': 50.0,        # mm body diameter  
    'sensor_shaft_diameter': 25.0,  # mm input/output shafts
    'sensor_range': '50_Nm',        # Nm - suitable for our motor
    'sensor_accuracy': 0.1,         # % full scale
    
    # Eddy Current Brake (Right Side)
    'brake_position_x': 850.0,      # mm from left edge
    'brake_disc_diameter': 200.0,   # mm - finned disc
    'brake_disc_thickness': 30.0,   # mm
    'brake_housing_width': 150.0,   # mm
    'brake_housing_height': 120.0,  # mm
    'brake_fin_count': 24,          # cooling fins on disc
    'brake_max_torque': 15.0,       # Nm
    
    # Shaft System
    'main_shaft_diameter': 25.0,    # mm - standard industrial size
    'main_shaft_length': 600.0,     # mm - spans motor to brake
    'shaft_material': 'Stainless_316',
    'shaft_surface_finish': 0.8,    # Ra μm
    
    # Bearing Pedestals (Professional Style)
    'pedestal_count': 3,            # Motor, sensor, brake
    'pedestal_height': 100.0,       # mm
    'pedestal_width': 80.0,         # mm
    'pedestal_depth': 120.0,        # mm
    'pedestal_material': 'Aluminum_6061_T6',
    'bearing_type': 'Ball_6005',    # 25mm bore
    'bearing_housing_type': 'Pillow_Block',
    
    # Coupling System
    'coupling_type': 'Flexible_Jaw',
    'coupling_bore': 25.0,          # mm
    'coupling_od': 65.0,            # mm
    'coupling_length': 40.0,        # mm
    'coupling_torque_rating': 20.0, # Nm
    
    # Data Acquisition (FUTEK Style)
    'daq_interface': 'USB520',      # FUTEK USB interface
    'display_type': 'IHH500',       # Handheld display
    'computer_interface': 'USB',    # PC connection
    'sampling_rate': 1000,          # Hz
    'data_logging': True,
    
    # Safety and Protection
    'guard_material': 'Polycarbonate',
    'guard_thickness': 5.0,         # mm
    'emergency_stop': True,
    'interlocks': True,
    'rotating_guard_coverage': '360_degree',
    
    # Electrical Components
    'motor_drive_type': 'Servo_Drive',
    'motor_drive_voltage': 48.0,    # V
    'motor_drive_current': 25.0,    # A
    'brake_controller_voltage': 24.0, # V
    'control_system': 'PLC_Based',
    
    # Performance Specifications
    'torque_measurement_range': '0-50_Nm',
    'speed_range': '0-3000_rpm',
    'measurement_accuracy': 0.1,    # % full scale
    'resolution': 0.01,             # Nm
    'bandwidth': 1000,              # Hz
    
    # Environmental
    'operating_temp_range': '15-40_degC',
    'humidity_max': 85,             # % RH
    'vibration_isolation': True,
    'noise_level_max': 65,          # dB
}

def generate_futek_style_report():
    """Generate comprehensive parameter report for FUTEK-style design"""
    print("="*70)
    print("FUTEK-STYLE HORIZONTAL MOTOR TEST BENCH PARAMETERS")
    print("Professional Configuration: Motor → Torque Sensor → Eddy Current Brake")  
    print("="*70)
    
    categories = {
        'Platform & Mechanical': [
            'base_length', 'base_width', 'base_height', 'base_material',
            'main_shaft_diameter', 'main_shaft_length', 'shaft_material'
        ],
        'Motor Integration': [
            'motor_position_x', 'motor_mount_height', 'motor_stator_diameter',
            'motor_stator_length', 'motor_shaft_extension'
        ],
        'Torque Sensor': [
            'sensor_type', 'sensor_position_x', 'sensor_range', 
            'sensor_accuracy', 'sensor_length', 'sensor_diameter'
        ],
        'Eddy Current Brake': [
            'brake_position_x', 'brake_disc_diameter', 'brake_disc_thickness',
            'brake_max_torque', 'brake_fin_count'
        ],
        'Bearing System': [
            'pedestal_count', 'pedestal_height', 'bearing_type',
            'bearing_housing_type', 'coupling_type'
        ],
        'Data Acquisition': [
            'daq_interface', 'display_type', 'sampling_rate',
            'measurement_accuracy', 'bandwidth'
        ],
        'Performance': [
            'torque_measurement_range', 'speed_range', 'resolution',
            'measurement_accuracy'
        ]
    }
    
    for category, params in categories.items():
        print(f"\n{category}:")
        for param in params:
            if param in FUTEK_PARAMETERS:
                value = FUTEK_PARAMETERS[param]
                print(f"  {param}: {value}")
    
    print("="*70)
    print(f"Total Parameters: {len(FUTEK_PARAMETERS)}")
    
    # Key design calculations
    print(f"\nKey Design Features:")
    total_length = FUTEK_PARAMETERS['base_length']
    motor_to_sensor = FUTEK_PARAMETERS['sensor_position_x'] - FUTEK_PARAMETERS['motor_position_x']  
    sensor_to_brake = FUTEK_PARAMETERS['brake_position_x'] - FUTEK_PARAMETERS['sensor_position_x']
    
    print(f"  Total bench length: {total_length} mm")
    print(f"  Motor to sensor span: {motor_to_sensor} mm")
    print(f"  Sensor to brake span: {sensor_to_brake} mm")
    print(f"  Torque capacity: {FUTEK_PARAMETERS['brake_max_torque']} Nm")
    print(f"  Measurement accuracy: ±{FUTEK_PARAMETERS['measurement_accuracy']}%")
    
    # Safety features
    print(f"\nSafety Features:")
    print(f"  Guard coverage: {FUTEK_PARAMETERS['rotating_guard_coverage']}")
    print(f"  Emergency stop: {FUTEK_PARAMETERS['emergency_stop']}")
    print(f"  Safety interlocks: {FUTEK_PARAMETERS['interlocks']}")
    
    print("="*70)

if __name__ == "__main__":
    generate_futek_style_report()