# Manufacturing Instructions - ILM-E85x30 Motor Test Bed

## Document Information
- **Project:** Assignment 1 - Motor Test Bed Design
- **Date:** 2025-08-06
- **Version:** 1.0
- **Status:** Ready for Manufacturing

## Overview
This document provides complete manufacturing instructions for the ILM-E85x30 motor test bed assembly. The design is based on 55 parametric parameters and engineered for precision torque measurement with ±0.25% system accuracy.

## Bill of Materials (BOM)

### Primary Structural Components

| Item | Description | Material | Quantity | Specifications |
|------|-------------|----------|----------|----------------|
| 1 | Base Frame | Cast Iron GG25 | 1 | 800×600×150mm, 180kg |
| 2 | Motor Housing | Aluminum 6061-T6 | 1 | Ø150×80mm, U6 bore fit |
| 3 | Main Shaft | Tool Steel D2 | 1 | Ø50×400mm, HRC 58-62 |
| 4 | Sensor Mount | Steel S355 | 1 | 200×150×25mm |
| 5 | Bearing Housings | Aluminum 6061-T6 | 2 | Custom machined |

### Precision Components

| Item | Description | Manufacturer | Part Number | Specifications |
|------|-------------|--------------|-------------|----------------|
| 6 | Precision Bearings | SKF | 7010 CD/P4A | P4 grade, 50×80×16mm |
| 7 | Torque Sensor | HBK | T210-10Nm | ±0.1%, IO-Link interface |
| 8 | Flexible Couplings | R+W | BK2-20-20 | Bellows type, ±0.5mm |
| 9 | Motor Controller | TQ-Group | Standard Drive | 48V, 25A capacity |
| 10 | Emergency Stop | Schneider | XB4BS8445 | IP65, NC contacts |

### Fasteners and Hardware

| Item | Description | Standard | Quantity | Specifications |
|------|-------------|----------|----------|----------------|
| 11 | Socket Head Screws | ISO 4762 | 20 | M10×40, Grade 12.9 |
| 12 | Hex Nuts | ISO 4032 | 20 | M10, Grade 8 |
| 13 | Washers | ISO 7089 | 40 | M10, Hardened |
| 14 | Dowel Pins | ISO 8734 | 8 | Ø8×30mm, Hardened |
| 15 | Thread Locker | Loctite | 243 | Medium strength |

## Manufacturing Sequence

### Phase 1: Base Frame Fabrication (Week 1-2)

#### 1.1 Base Frame Casting
- **Process:** Sand casting or machining from solid block
- **Material:** Cast Iron GG25 (minimum tensile strength 250 MPa)
- **Dimensions:** 800×600×150mm ±1mm
- **Features:**
  - 4× Ø16mm holes for leveling feet (M12 threads)
  - 6× Ø12mm precision holes for motor mount
  - Internal ribs for rigidity (see CAD model)

#### 1.2 Base Frame Machining
- **Primary Operations:**
  - Face milling top surface (Ra 3.2μm)
  - Drill and tap mounting holes
  - Bore precision holes (±0.02mm)
- **Quality Control:**
  - CMM inspection of all hole positions
  - Surface roughness verification
  - Flatness check (±0.05mm over surface)

### Phase 2: Motor Housing Manufacturing (Week 2)

#### 2.1 Housing Blank Preparation
- **Material:** Aluminum 6061-T6 round bar, Ø160×100mm
- **Process:** Turn to rough dimensions

#### 2.2 Precision Machining
```
Operation Sequence:
1. Face both ends to 80mm ±0.05mm length
2. Turn OD to Ø150mm ±0.1mm
3. Bore ID to Ø85mm U6 tolerance (-0.117/-0.139mm)
4. Machine cooling fin grooves (12 fins, 15mm deep)
5. Drill mounting holes (6×M8×1.25)
6. Final inspection and deburring
```

#### 2.3 Critical Tolerances
- **Bore Concentricity:** ±0.02mm TIR to OD
- **Surface Finish:** Ra 1.6μm on bore surface
- **Roundness:** ±0.01mm on bore and OD

### Phase 3: Shaft System Manufacturing (Week 2-3)

#### 3.1 Shaft Blank Preparation
- **Material:** Tool Steel D2, Ø55×450mm
- **Heat Treatment:** Harden to HRC 58-62

#### 3.2 Precision Turning
```
Operation Sequence:
1. Turn between centers to Ø50mm ±0.005mm
2. Machine bearing seats (2 locations)
3. Machine coupling interfaces (both ends)
4. Grind to final dimensions and surface finish
5. Dynamic balancing to G2.5 grade
```

#### 3.3 Quality Requirements
- **Straightness:** ±0.01mm over 400mm length
- **Surface Finish:** Ra 0.4μm on bearing surfaces
- **Concentricity:** All diameters within ±0.005mm TIR

### Phase 4: Precision Components Assembly (Week 3)

#### 4.1 Bearing Installation
- **Process:** Thermal installation (80°C bearing temperature)
- **Preload:** 50-100N axial force using precision spacers
- **Lubrication:** SKF LGEP 2/0.4 high-speed grease (0.5g per bearing)

#### 4.2 Housing Assembly
- **Motor Stator Fit:** Hydraulic press with alignment mandrel
- **Press Force:** 2-5 tons gradual application
- **Verification:** Dial indicator check for ±0.02mm TIR

## Assembly Procedures

### Step 1: Base Frame Setup
1. Install leveling feet and adjust to ±0.1mm level
2. Mount vibration isolation pads
3. Install motor housing mounting brackets
4. Verify geometric alignment with CMM

### Step 2: Shaft System Assembly
1. Install bearings on shaft with proper preload
2. Mount shaft assembly in bearing housings
3. Check runout (must be <0.02mm TIR)
4. Connect flexible couplings

### Step 3: Motor Integration
1. Press-fit motor stator into housing
2. Insert rotor onto shaft (1mm clearance all around)
3. Check air gap uniformity (±0.1mm)
4. Connect electrical harnesses

### Step 4: Sensor Installation
1. Mount torque sensor between motor and load
2. Align coupling interfaces (±0.02mm concentricity)
3. Connect sensor cables with proper shielding
4. Calibrate zero point and verify range

### Step 5: Safety Systems
1. Install emergency stop circuit
2. Mount rotating guards and interlocks
3. Connect temperature monitoring sensors
4. Test all safety functions

## Quality Control Checkpoints

### Dimensional Verification
- [ ] Base frame dimensions and hole positions
- [ ] Motor housing bore size and concentricity  
- [ ] Shaft diameter and straightness
- [ ] All threaded connections torqued to specification

### Alignment Verification
- [ ] Motor-to-shaft concentricity <0.02mm TIR
- [ ] Sensor coupling alignment <0.02mm
- [ ] Base frame levelness <0.1mm
- [ ] Shaft runout <0.02mm TIR

### Performance Testing
- [ ] Torque sensor calibration verification
- [ ] Temperature monitoring system check
- [ ] Emergency stop function test
- [ ] Motor rotation test (low speed)

## Material Certificates Required
- Cast iron material certification (chemistry and properties)
- Aluminum 6061-T6 mill certificate
- Tool steel D2 heat treatment certificate
- Bearing precision grade certificate
- Torque sensor calibration certificate

## Special Tooling Required
- Hydraulic press (5-ton minimum)
- Precision boring head
- CMM for dimensional verification
- Dial indicators (0.001mm resolution)
- Torque wrench set
- Bearing heater
- Dynamic balancing machine

## Testing and Commissioning

### Initial Testing Protocol
1. **Static Tests:**
   - Dimensional verification
   - Alignment checks
   - Electrical continuity
   - Safety system function

2. **Dynamic Tests:**
   - Low-speed rotation (100 rpm)
   - Vibration measurement
   - Temperature monitoring
   - Torque measurement accuracy

3. **Performance Validation:**
   - Full speed test (2500 rpm)
   - Torque range verification (0-8 Nm)
   - Long-term stability (4-hour run)
   - Data acquisition system check

### Acceptance Criteria
- **Torque Accuracy:** ±0.25% of reading
- **Vibration:** <0.1mm/s RMS
- **Temperature Rise:** <30°C above ambient
- **Safety Response:** <1 second emergency stop

## Documentation Deliverables

### Manufacturing Records
- [ ] Material certificates for all components
- [ ] Dimensional inspection reports
- [ ] Heat treatment certificates
- [ ] Assembly photographs and notes
- [ ] Final acceptance test report

### Operational Documentation
- [ ] Assembly drawings (CAD-generated)
- [ ] Operating procedures manual
- [ ] Maintenance schedule
- [ ] Troubleshooting guide
- [ ] Parts list with supplier information

## Risk Assessment and Mitigation

### High-Risk Operations
1. **Motor Stator Press Fit**
   - Risk: Damage to stator windings
   - Mitigation: Use alignment mandrel, gradual pressure

2. **Shaft Machining**
   - Risk: Dimensional errors affecting bearing fit
   - Mitigation: Multiple inspection points, qualified machinist

3. **Bearing Installation**
   - Risk: Bearing damage during installation
   - Mitigation: Thermal installation method, proper tools

### Quality Risks
- **Alignment Errors:** Use CMM verification at each stage
- **Material Defects:** Require certificates for all materials
- **Assembly Errors:** Documented procedures and checkpoints

## Cost Breakdown

### Manufacturing Costs (Estimated)
- Materials: $15,000
- Machining: $8,000  
- Assembly Labor: $3,000
- Quality Control: $2,000
- **Total Manufacturing:** $28,000

### Equipment and Tooling
- Precision instruments: $5,000
- Special tooling: $2,000
- **Total Equipment:** $7,000

### **Project Total:** $35,000

## Schedule Summary
- **Week 1-2:** Base frame and housing manufacture
- **Week 2-3:** Shaft system machining and heat treatment
- **Week 3:** Precision assembly and alignment
- **Week 4:** Testing, commissioning, and documentation

**Total Project Duration:** 4 weeks

---

**Approval Required:**
- [ ] Design Engineer: _________________ Date: _______
- [ ] Manufacturing Engineer: __________ Date: _______  
- [ ] Quality Manager: ________________ Date: _______
- [ ] Project Manager: ________________ Date: _______