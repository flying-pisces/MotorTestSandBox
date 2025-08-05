# FreeCAD Parametric Test Bed Design Concept

## Design Overview

The test bed is designed as a modular, parametric assembly in FreeCAD to measure and record output torque of the ILM-E85x30 frameless motor. The design emphasizes precision alignment, thermal management, and data acquisition accuracy.

## Main Assembly Components

### 1. Base Frame Assembly
**Purpose:** Rigid foundation and vibration isolation  
**Material:** Cast iron or welded steel construction  
**Key Features:**
- Parametric dimensions: 800mm × 600mm × 150mm (L×W×H)
- Integrated leveling feet with vibration dampers
- Precision machined surfaces for component mounting
- Access panels for wiring and maintenance

### 2. Motor Housing Assembly
**Purpose:** Precision mounting of ILM-E85x30 stator  
**Material:** Aluminum 6061-T6 (per motor requirements)  
**Key Specifications:**
- **Stator Bore:** Ø85 U6 (-0.117/-0.139) for press fit mounting
- **Housing OD:** Ø150mm for robust construction
- **Length:** 80mm to accommodate 44.4mm stator + clearance
- **Cooling Fins:** Integrated for thermal management
- **Positioning:** 2 × Ø2mm H9 holes for precise alignment

**Parametric Features:**
- Adjustable mounting height: 100-200mm from base
- Angular positioning: 0-360° adjustment capability
- Thermal expansion compensation

### 3. Rotor Shaft Assembly
**Purpose:** Precision shaft system for motor rotor  
**Material:** Hardened steel (HRC 58-62)  
**Design:**
- **Shaft Diameter:** Ø50mm (fits 52mm hollow rotor with 1mm clearance)
- **Length:** 400mm total (extends both sides of motor)
- **Bearings:** Precision angular contact bearings (SKF 7010 or equivalent)
- **Coupling Interface:** ISO standard coupling hub

**Critical Tolerances:**
- Concentricity: ±0.02mm TIR
- Parallelism: ±0.05mm over shaft length
- Surface finish: Ra 0.4μm

### 4. Torque Sensor Mount
**Purpose:** Precision mounting of HBK T210-10Nm sensor  
**Design Features:**
- **Input Coupling:** Connects to motor rotor shaft
- **Output Coupling:** Connects to load brake/dynamometer
- **Alignment System:** Kinematic mounting for repeatable positioning
- **Environmental Protection:** IP65 rated enclosure option

### 5. Load System
**Purpose:** Controllable load for torque testing  
**Options:**
- **Hysteresis Brake:** 0-15 Nm capacity, air or water cooled
- **Servo Brake:** Regenerative capability, precise control
- **Powder Brake:** Cost-effective, good heat dissipation

### 6. Data Acquisition Enclosure
**Purpose:** Electronics housing and control interface  
**Contents:**
- Motor drive controller (48V, 25A capacity)
- Torque sensor interface (IO-Link master)
- Temperature monitoring (thermocouples, RTDs)
- Safety interlocks and emergency stop
- Data logging computer/PLC

## FreeCAD Parametric Design Strategy

### Master Parameters Spreadsheet
```
# Base Dimensions
Base_Length = 800mm
Base_Width = 600mm  
Base_Height = 150mm

# Motor Specifications
Motor_Stator_Diameter = 85mm
Motor_Stator_Length = 44.4mm
Motor_Rotor_Bore = 52mm
Motor_Housing_Fit = U6 (parametric tolerance)

# Shaft System
Shaft_Diameter = 50mm
Bearing_Type = "7010" (angular contact)
Coupling_Type = "ISO_Standard"

# Sensor Interface
Sensor_Model = "HBK_T210_10Nm"
Sensor_Length = 150mm (estimated)
Coupling_Torque_Rating = 15Nm

# Safety Factors
Torque_Safety_Factor = 1.5
Speed_Safety_Factor = 2.0
```

### Parametric Constraints
1. **Alignment Chain:** Base → Motor Housing → Shaft → Sensor → Load
2. **Thermal Expansion:** Temperature compensation in all interfaces
3. **Accessibility:** Minimum 100mm clearance for maintenance
4. **Safety:** Guards and interlocks on all rotating components

## Critical Design Features

### 1. Precision Alignment System
**Motor-to-Shaft Alignment:**
- Kinematic mount with 3-point contact
- Adjustable shims for angular correction
- Dial indicator points for setup verification
- Repeatable positioning within ±0.01mm

**Sensor-to-Shaft Alignment:**
- Floating coupling design accommodates minor misalignment  
- Bellows coupling isolates axial forces
- Temperature-stable materials prevent drift

### 2. Thermal Management
**Motor Cooling:**
- Aluminum housing with integrated cooling fins
- Optional forced air cooling (24V fans)
- Temperature monitoring at 4 locations
- Thermal protection circuits

**Sensor Protection:**
- Heat shields between motor and sensor
- Thermal barrier coatings
- Active cooling for extended testing

### 3. Vibration Isolation
**Base Isolation:**
- Pneumatic or rubber isolators
- Natural frequency <5Hz
- Damping ratio 0.1-0.2

**Component Isolation:**
- Flexible couplings in drive train
- Vibration-damped mounting brackets
- Separate foundations for sensitive components

## Assembly Sequence

### Phase 1: Base Preparation
1. Install base frame on isolators
2. Level base to ±0.05mm over entire surface
3. Install main bearing pedestals
4. Verify geometric alignment

### Phase 2: Shaft System
1. Install precision bearings with proper preload
2. Mount and align shaft assembly
3. Verify concentricity and parallelism
4. Install shaft seals and guards

### Phase 3: Motor Integration
1. Press-fit stator into aluminum housing
2. Install housing on adjustable mount
3. Insert rotor into shaft system
4. Verify air gap uniformity (±0.1mm)

### Phase 4: Sensor Installation
1. Install torque sensor between motor and load
2. Connect with precision couplings
3. Verify sensor calibration and zero point
4. Test measurement system integrity

### Phase 5: Control System
1. Install drive electronics and safety systems
2. Connect all sensors and feedback devices
3. Commission control software
4. Perform system verification tests

## Design Validation

### Structural Analysis
- FEA analysis of base frame under maximum loads
- Modal analysis to verify natural frequencies >50Hz
- Thermal analysis of motor housing under full load

### Alignment Verification
- CMM measurement of as-built geometry
- Shaft runout measurement
- Motor air gap verification
- Sensor coupling alignment check

### Performance Testing
- Torque measurement accuracy verification
- Speed measurement calibration
- Temperature monitoring validation
- Safety system functional testing

## Material Specifications

### Primary Structure
- **Base Frame:** Cast iron (GG25) or welded steel (S355)
- **Motor Housing:** Aluminum 6061-T6
- **Shaft:** Tool steel (1.2379/D2) hardened to HRC 58-62
- **Bearings:** Precision grade (P4 or better)

### Secondary Components
- **Couplings:** Steel or aluminum depending on application
- **Guards:** Transparent polycarbonate or aluminum sheet
- **Fasteners:** Stainless steel 316 or equivalent

## Cost Estimation

### Major Components
- **Base Frame:** $2,000-3,000
- **Motor Housing:** $1,500-2,000  
- **Shaft System:** $3,000-4,000
- **Torque Sensor:** $8,000-12,000
- **Load Brake:** $5,000-8,000
- **Controls:** $3,000-5,000

**Total Estimated Cost:** $22,500-34,000 USD

## Next Steps

1. **Detailed FreeCAD Modeling:** Create parametric assembly with full constraints
2. **Engineering Drawings:** Generate manufacturing drawings from 3D model
3. **Supplier Selection:** Identify vendors for custom machining
4. **Procurement:** Order long-lead-time items (torque sensor, precision bearings)
5. **Manufacturing:** Begin fabrication of custom components