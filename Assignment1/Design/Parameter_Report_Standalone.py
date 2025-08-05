#!/usr/bin/env python3
"""
Standalone Parameter Report for ILM-E85x30 Motor Test Bed
Generates design parameter report without FreeCAD dependencies
"""

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

def generate_parameter_report():
    """Generate a comprehensive report of all design parameters"""
    print("\n" + "="*70)
    print("FREECAD PARAMETRIC MOTOR TEST BED DESIGN PARAMETERS")
    print("="*70)
    print(f"Design Target: ILM-E85x30 Frameless Motor Test Bed")
    print(f"Design Philosophy: Parametric, modular, high-precision")
    print(f"Analysis Date: 2025-08-04")
    
    categories = {
        'Base Frame Parameters': [
            'base_length', 'base_width', 'base_height', 
            'base_material', 'base_mass'
        ],
        'Motor Specifications (ILM-E85x30)': [
            'motor_stator_diameter', 'motor_stator_length', 'motor_rotor_bore',
            'motor_rotor_length', 'motor_mass', 'motor_rated_torque', 
            'motor_peak_torque', 'motor_max_speed'
        ],
        'Motor Housing Design': [
            'housing_outer_diameter', 'housing_length', 'housing_bore_diameter',
            'housing_bore_tolerance', 'housing_material', 'housing_cooling_fins',
            'housing_fin_height', 'housing_fin_count'
        ],
        'Precision Shaft System': [
            'shaft_diameter', 'shaft_length', 'shaft_material',
            'shaft_hardness', 'shaft_surface_finish'
        ],
        'Bearing Specifications': [
            'bearing_type', 'bearing_bore', 'bearing_outer_diameter',
            'bearing_width', 'bearing_precision_grade'
        ],
        'Torque Sensor Interface': [
            'sensor_model', 'sensor_range', 'sensor_accuracy',
            'sensor_length', 'sensor_input_shaft', 'sensor_output_shaft'
        ],
        'Load System': [
            'load_type', 'load_torque_capacity', 'load_speed_capacity',
            'load_cooling'
        ],
        'Safety & Design Factors': [
            'torque_safety_factor', 'speed_safety_factor', 
            'structural_safety_factor'
        ],
        'Precision & Tolerances': [
            'alignment_tolerance', 'parallelism_tolerance', 
            'position_repeatability'
        ],
        'Control System': [
            'motor_drive_voltage', 'motor_drive_current',
            'data_acquisition_rate', 'temperature_sensors'
        ],
        'Environmental Conditions': [
            'operating_temp_min', 'operating_temp_max',
            'humidity_max', 'vibration_isolation_freq'
        ]
    }
    
    for category, params in categories.items():
        print(f"\n{category}:")
        print("-" * len(category))
        for param in params:
            if param in DESIGN_PARAMETERS:
                value = DESIGN_PARAMETERS[param]
                param_display = param.replace('_', ' ').title()
                print(f"  {param_display:.<35} {value}")
    
    print("\n" + "="*70)

def calculate_design_metrics():
    """Calculate key design metrics and ratios"""
    print("\nDESIGN ANALYSIS & METRICS")
    print("="*70)
    
    # Torque capacity analysis
    motor_peak = DESIGN_PARAMETERS['motor_peak_torque']
    sensor_range = DESIGN_PARAMETERS['sensor_range']
    load_capacity = DESIGN_PARAMETERS['load_torque_capacity']
    
    print(f"\nTorque Capacity Analysis:")
    print(f"  Motor Peak Torque:............ {motor_peak} Nm")
    print(f"  Sensor Range:................. {sensor_range} Nm")
    print(f"  Load Capacity:................ {load_capacity} Nm")
    print(f"  Sensor Margin:................ {((sensor_range/motor_peak)-1)*100:.1f}%")
    print(f"  Load Margin:.................. {((load_capacity/motor_peak)-1)*100:.1f}%")
    
    # Speed analysis
    motor_speed = DESIGN_PARAMETERS['motor_max_speed']
    load_speed = DESIGN_PARAMETERS['load_speed_capacity']
    
    print(f"\nSpeed Capacity Analysis:")
    print(f"  Motor Max Speed:.............. {motor_speed} rpm")
    print(f"  Load Speed Capacity:.......... {load_speed} rpm")
    print(f"  Speed Margin:................. {((load_speed/motor_speed)-1)*100:.1f}%")
    
    # Dimensional analysis
    base_area = DESIGN_PARAMETERS['base_length'] * DESIGN_PARAMETERS['base_width'] / 1000000  # m²
    base_volume = base_area * DESIGN_PARAMETERS['base_height'] / 1000  # m³
    
    print(f"\nPhysical Dimensions:")
    print(f"  Base Footprint:............... {base_area:.2f} m²")
    print(f"  Base Volume:.................. {base_volume:.3f} m³")
    print(f"  Estimated Total Mass:......... {DESIGN_PARAMETERS['base_mass']:.0f} kg")
    print(f"  Power Density:................ {446/base_volume:.0f} W/m³")
    
    # Precision analysis
    shaft_dia = DESIGN_PARAMETERS['shaft_diameter']
    alignment_tol = DESIGN_PARAMETERS['alignment_tolerance']
    
    print(f"\nPrecision Analysis:")
    print(f"  Shaft Diameter:............... {shaft_dia} mm")
    print(f"  Alignment Tolerance:.......... ±{alignment_tol} mm TIR")
    print(f"  Relative Precision:........... {(alignment_tol/shaft_dia)*100:.3f}%")
    print(f"  Sensor Accuracy:.............. ±{DESIGN_PARAMETERS['sensor_accuracy']}%")

def generate_freecad_instructions():
    """Generate instructions for FreeCAD implementation"""
    print("\nFREECAD IMPLEMENTATION INSTRUCTIONS")
    print("="*70)
    
    print("""
1. SETUP PARAMETRIC SPREADSHEET:
   - Create new FreeCAD document: 'MotorTestBed'
   - Insert Spreadsheet object: 'DesignParameters'  
   - Import all parameters from DESIGN_PARAMETERS dictionary
   - Use cell references for all dimensions (e.g., =A1, =B2)

2. CREATE BASE FRAME:
   - Start with PartDesign Body: 'BaseFrame'
   - Sketch rectangular base: length x width from parameters
   - Pad to base_height
   - Add mounting holes and leveling feet locations
   - Apply Cast Iron material properties

3. CREATE MOTOR HOUSING:
   - New PartDesign Body: 'MotorHousing'
   - Sketch concentric circles: outer_diameter and bore_diameter
   - Pad to housing_length
   - Add cooling fins using Polar Pattern
   - Apply Aluminum 6061-T6 material

4. CREATE SHAFT ASSEMBLY:
   - New PartDesign Body: 'MainShaft'
   - Sketch circle: shaft_diameter
   - Pad to shaft_length
   - Add bearing seats and coupling interfaces
   - Apply Tool Steel material with hardness notes

5. CREATE SENSOR MOUNT:
   - New PartDesign Body: 'SensorMount'
   - Design kinematic mount for HBK T210 sensor
   - Include adjustment mechanisms
   - Add cable management features

6. ASSEMBLY CONSTRAINTS:
   - Use Assembly4 or A2plus workbench
   - Define concentricity constraints: shaft to housing
   - Add parallelism constraints: base to shaft axis
   - Include thermal expansion allowances

7. ANALYSIS FEATURES:
   - FEM workbench: structural analysis of base frame
   - CFD analysis: thermal management of motor housing
   - Motion study: dynamic behavior verification

8. DOCUMENTATION:
   - TechDraw workbench: generate 2D drawings
   - Include GD&T symbols for critical tolerances
   - Create assembly drawings with part lists
   - Generate manufacturing drawings for custom parts
""")

def export_parameters_csv():
    """Export parameters to CSV for external use"""
    import csv
    from datetime import datetime
    
    filename = f"../Documentation/Design_Parameters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Parameter', 'Value', 'Unit/Type', 'Category'])
        
        categories = {
            'Base Frame': ['base_length', 'base_width', 'base_height', 'base_material', 'base_mass'],
            'Motor': ['motor_stator_diameter', 'motor_stator_length', 'motor_rotor_bore', 'motor_rated_torque'],
            'Housing': ['housing_outer_diameter', 'housing_length', 'housing_material'],
            'Shaft': ['shaft_diameter', 'shaft_length', 'shaft_material'],
            'Sensor': ['sensor_model', 'sensor_range', 'sensor_accuracy'],
            'Tolerances': ['alignment_tolerance', 'parallelism_tolerance']
        }
        
        for category, params in categories.items():
            for param in params:
                if param in DESIGN_PARAMETERS:
                    value = DESIGN_PARAMETERS[param]
                    # Determine unit
                    if 'diameter' in param or 'length' in param or 'height' in param or 'width' in param:
                        unit = 'mm'
                    elif 'torque' in param:
                        unit = 'Nm'
                    elif 'speed' in param:
                        unit = 'rpm'
                    elif 'mass' in param:
                        unit = 'kg'
                    elif 'accuracy' in param or 'tolerance' in param:
                        unit = 'mm' if isinstance(value, (int, float)) and value < 1 else '%'
                    else:
                        unit = 'various'
                    
                    writer.writerow([param, value, unit, category])
    
    print(f"\nParameters exported to: {filename}")

if __name__ == "__main__":
    # Generate comprehensive parameter report
    generate_parameter_report()
    
    # Calculate design metrics
    calculate_design_metrics()
    
    # Generate FreeCAD instructions
    generate_freecad_instructions()
    
    # Export to CSV
    export_parameters_csv()
    
    print(f"\nParametric design analysis complete!")
    print(f"Total parameters defined: {len(DESIGN_PARAMETERS)}")
    print(f"Ready for FreeCAD implementation.")