# Test Procedure: ILM-E85x30 Motor Torque Measurement

## Purpose and Scope

This document provides detailed procedures for mounting the ILM-E85x30 frameless motor in the test bed and measuring its output torque across varying load conditions. The procedure ensures accurate, repeatable measurements while maintaining safety and protecting equipment.

## Test Equipment Required

### Primary Equipment
- **Motor Under Test:** TQ-Group ILM-E85x30 frameless servo kit
- **Test Bed Assembly:** Custom parametric design (FreeCAD model)
- **Torque Sensor:** HBK T210-10Nm with IO-Link interface
- **Load System:** Hysteresis brake (15 Nm capacity)
- **Motor Drive:** 48V, 25A servo amplifier

### Instrumentation
- **Data Acquisition:** IO-Link master with 1 kHz sampling
- **Temperature Monitoring:** 6 x Type-K thermocouples
- **Position Feedback:** Absolute encoder (optional)
- **Oscilloscope:** For electrical signal analysis
- **Multimeter:** For voltage/current verification

### Safety Equipment
- **Emergency Stop:** Hardwired system with redundant contacts
- **Safety Guards:** Transparent polycarbonate covers
- **Personal Protection:** Safety glasses, hearing protection
- **First Aid Kit:** Readily accessible

## Pre-Test Setup Procedures

### 1. Test Bed Preparation
**Duration:** 30 minutes  
**Personnel:** 2 technicians

1. **Visual Inspection**
   - Verify all mounting bolts are tight (torque spec: per assembly drawing)
   - Check alignment indicators on shaft system
   - Inspect electrical connections for damage
   - Verify emergency stop functionality

2. **Baseline Measurements**
   - Record ambient temperature: ______°C
   - Measure shaft runout: ______mm TIR (spec: <0.02mm)
   - Verify torque sensor zero point: ______Nm (should be <0.01Nm)
   - Check bearing temperature: ______°C (should match ambient)

3. **System Calibration**
   - Perform torque sensor zero calibration
   - Verify temperature sensor readings against reference
   - Test data acquisition system connectivity
   - Confirm load brake operation (manual control)

### 2. Motor Installation
**Duration:** 45 minutes  
**Personnel:** 2 technicians

1. **Stator Installation**
   ```
   CRITICAL: Handle stator with extreme care - precision component
   ```
   - Clean motor housing bore with lint-free cloth
   - Apply thin layer of thermal compound (if specified)
   - Press-fit stator into housing using hydraulic press
   - **Press Force:** 2-5 tons (monitor fit progress)
   - **Alignment:** Use precision fixture to maintain concentricity
   - Verify stator depth: 44.4mm ± 0.1mm from housing face

2. **Rotor Installation**
   ```
   WARNING: Strong magnets - keep metal objects away
   ```
   - Slide rotor carefully onto precision shaft
   - **Clearance Check:** Verify 1mm gap between rotor and stator
   - **Axial Position:** Center rotor within stator (±0.2mm)
   - **Air Gap Measurement:** Use feeler gauges at 4 positions
     - Position 1 (0°): ______mm
     - Position 2 (90°): ______mm  
     - Position 3 (180°): ______mm
     - Position 4 (270°): ______mm
     - **Specification:** 1.0mm ± 0.1mm (uniform)

3. **Electrical Connections**
   - Connect 3-phase power cables (A, B, C phases)
   - Attach Hall sensor cables (SA1, SA2, SA3)
   - Connect temperature sensors (SP1, SP2)
   - **Insulation Test:** 1000V DC for 1 minute (>10MΩ)
   - **Phase Resistance:** Measure R(A-B), R(B-C), R(C-A)
     - Star-Serial: ~387mΩ ± 10%
     - Record values: R(A-B)=______, R(B-C)=______, R(C-A)=______

## Test Procedures

### Test 1: Static Torque Calibration
**Objective:** Verify torque measurement accuracy  
**Duration:** 20 minutes

1. **Known Load Application**
   - Apply calibrated weights to torque arm (radius = 100mm)
   - Test points: 0.5, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0 Nm
   - Record sensor reading vs. applied torque
   - **Acceptance:** ±0.1% accuracy across range

2. **Hysteresis Check**
   - Apply increasing torque: 0 → 10 Nm
   - Apply decreasing torque: 10 → 0 Nm
   - **Acceptance:** <0.05% hysteresis error

### Test 2: Motor Characterization Tests
**Objective:** Measure motor torque across operating range  
**Duration:** 2 hours

#### Test 2A: Torque vs. Current (Locked Rotor)
**Safety Note:** Limit test duration to prevent overheating

1. **Setup**
   - Lock rotor using mechanical brake
   - Set motor drive to current control mode
   - **Maximum Test Current:** 80% of rated (limit thermal stress)

2. **Test Procedure**
   ```
   FOR each current level (10%, 20%, 30%, 50%, 70%, 80% of rated):
     1. Apply current for 10 seconds maximum
     2. Record: Current (A), Torque (Nm), Temperature (°C)
     3. Allow 2-minute cooling between tests
     4. Stop if temperature exceeds 80°C
   END FOR
   ```

3. **Data Recording Template**
   | Current (A) | Torque (Nm) | Temp Rise (°C) | Notes |
   |-------------|-------------|----------------|-------|
   | 1.08 (10%)  |             |                |       |
   | 2.16 (20%)  |             |                |       |
   | 3.24 (30%)  |             |                |       |
   | 5.40 (50%)  |             |                |       |
   | 7.56 (70%)  |             |                |       |
   | 8.64 (80%)  |             |                |       |

#### Test 2B: Torque vs. Speed (Variable Load)
**Objective:** Map torque-speed characteristics

1. **Setup**
   - Configure load brake for variable torque control
   - Set motor drive to speed control mode
   - **Speed Range:** 100-2000 rpm (avoid resonances)

2. **Test Matrix**
   ```
   FOR each speed (100, 250, 500, 750, 1000, 1500, 2000 rpm):
     FOR each torque level (0.5, 1.0, 2.0, 3.0 Nm):
       1. Set target speed and load torque
       2. Allow 30 seconds for stabilization  
       3. Record data for 10 seconds (1 kHz sampling)
       4. Calculate: Average torque, torque ripple, efficiency
     END FOR
   END FOR
   ```

3. **Key Measurements**
   - **Motor Torque:** HBK sensor reading
   - **Speed:** Encoder feedback
   - **Electrical Power:** V × I × cos(φ)
   - **Mechanical Power:** Torque × Angular velocity
   - **Efficiency:** P_mechanical / P_electrical

#### Test 2C: Dynamic Response Tests
**Objective:** Characterize transient torque behavior

1. **Step Response Test**
   - Apply step torque command: 0 → 2 Nm → 0 Nm
   - **Step Duration:** 1 second each
   - **Sampling Rate:** 1 kHz
   - **Measurements:** Rise time, overshoot, settling time

2. **Sinusoidal Response Test**
   - Apply sinusoidal torque command: 1 ± 0.5 Nm
   - **Frequencies:** 1, 5, 10, 20, 50 Hz
   - **Measurements:** Magnitude ratio, phase lag, distortion

### Test 3: Thermal Performance
**Objective:** Evaluate thermal behavior under load  
**Duration:** 1 hour

1. **Heat Run Test**
   - **Load Condition:** 3.3 Nm at 1000 rpm (rated conditions)
   - **Duration:** 60 minutes continuous
   - **Monitoring:** Temperature every 30 seconds

2. **Temperature Limits**
   - **Stator Winding:** <125°C (per specification)
   - **Housing:** <80°C (safe handling)
   - **Bearings:** <70°C (lubrication limit)
   - **Ambient:** Record initial temperature

3. **Thermal Time Constant**
   - Measure time to reach 63% of final temperature rise
   - **Specification:** Typically 5-15 minutes for this motor size

## Data Analysis Procedures

### 1. Torque Accuracy Assessment
- **Linearity Error:** Calculate deviation from best-fit line
- **Hysteresis:** Maximum difference between up/down measurements  
- **Repeatability:** Standard deviation of repeat measurements
- **Resolution:** Smallest detectable torque change

### 2. Motor Performance Calculations
```
Torque Constant (kt) = Torque / Current [Nm/A]
Speed Constant (kv) = Speed / Voltage [rpm/V]  
Efficiency (η) = P_mechanical / P_electrical [%]
Power Factor (PF) = P_real / P_apparent
Torque Ripple = (T_max - T_min) / T_average [%]
```

### 3. Statistical Analysis
- **Mean Values:** Average of all measurements per test point
- **Standard Deviation:** Measure of data scatter
- **Confidence Intervals:** 95% confidence bounds
- **Correlation Analysis:** Relationships between variables

## Post-Test Procedures

### 1. System Shutdown
1. **Gradual Shutdown**
   - Reduce load to zero over 30 seconds
   - Stop motor with controlled deceleration
   - Turn off drive power after motion stops
   - Allow components to cool before handling

2. **Data Backup**
   - Save all test data to network storage
   - Export key results to analysis software
   - Generate automated test report
   - Archive calibration certificates

### 2. Equipment Inspection
1. **Motor Condition**
   - Visual inspection for damage or wear
   - Check electrical connections for looseness
   - Verify insulation resistance (should remain >10MΩ)
   - Document any anomalies

2. **Test Bed Status**
   - Check torque sensor calibration drift
   - Verify shaft alignment hasn't changed
   - Inspect bearings for temperature, noise, vibration
   - Clean and prepare for next test

## Quality Control and Validation

### Acceptance Criteria
- **Torque Accuracy:** ±0.5% of reading or ±0.01 Nm, whichever is greater
- **Speed Accuracy:** ±0.1% of reading
- **Temperature Stability:** <2°C drift during test
- **Data Integrity:** <0.1% missing or corrupt data points

### Calibration Requirements
- **Torque Sensor:** Annual calibration to NIST standards
- **Temperature Sensors:** Quarterly calibration check
- **Speed Measurement:** Semi-annual encoder calibration
- **Load Brake:** Annual torque calibration

### Documentation Requirements
- **Test Report:** Comprehensive analysis with all results
- **Raw Data:** Complete dataset archived for future reference
- **Calibration Records:** Current certificates for all instruments
- **Anomaly Reports:** Document any unexpected behavior

## Safety Considerations

### Electrical Hazards
- **High Voltage:** 48V DC drive voltage
- **High Current:** Up to 25A motor current
- **Rotating Equipment:** Exposed shaft and coupling
- **Magnetic Fields:** Strong permanent magnets in rotor

### Mechanical Hazards
- **Rotating Machinery:** 2500+ rpm operation
- **Pinch Points:** Coupling interfaces
- **Heavy Components:** 180kg test bed mass
- **Stored Energy:** Rotating inertia, compressed air

### Emergency Procedures
1. **Emergency Stop:** Hit red button - cuts all power
2. **Fire:** Use CO2 extinguisher (electrical equipment)
3. **Injury:** First aid kit location: _______________
4. **Equipment Damage:** Stop test, secure area, report

## Troubleshooting Guide

### Common Issues
| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| High torque noise | Misalignment | Check shaft coupling alignment |
| Sensor drift | Temperature effects | Allow thermal stabilization |
| Erratic readings | Electrical interference | Check cable shielding |
| Vibration | Unbalanced rotor | Verify rotor installation |
| Overheating | Insufficient cooling | Check airflow, reduce load |

### Calibration Checks
- **Zero Drift:** Should be <0.01 Nm over 1 hour
- **Span Error:** Should be <0.1% at full scale
- **Linearity:** Should be <0.05% of full scale
- **Temperature Coefficient:** <0.01%/°C typical

---

**Document Control:**
- **Version:** 1.0
- **Date:** 2025-08-04  
- **Author:** Assignment 1 Team
- **Approved By:** Test Engineer
- **Next Review:** 2026-08-04