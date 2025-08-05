# Torque Sensor Selection for ILM-E85x30 Test Bed

## Requirements Analysis

### Motor Specifications Recap
- **Rated Torque:** 3.3 N⋅m
- **Peak Torque:** 10.64 N⋅m
- **Max Speed:** 2,570 rpm
- **Required Measurement Range:** 0-15 N⋅m (with safety margin)

### Sensor Requirements
- **Torque Range:** 0-10 N⋅m minimum (covers peak torque + margin)
- **Accuracy:** ±0.1% or better for precision testing
- **Speed Rating:** ≥3,000 rpm to cover motor speed range
- **Output:** Digital preferred for data acquisition
- **Mounting:** Shaft-to-shaft configuration for test bed integration

## Recommended Sensor: HBK T210-10 Nm

### Key Specifications
- **Torque Range:** 10 N⋅m nominal
- **Accuracy Class:** 0.1 (±0.1% of full scale)
- **Linearity:** ≤ ±0.05% of full scale
- **Maximum Speed:** 30,000 rpm (well above motor requirements)
- **Measuring Bandwidth:** Up to 1 kHz

### Output Options
1. **IO-Link Digital Output** (Recommended)
   - Process data: Torque, speed, angle, power, temperature
   - Two configurable digital limit switches
   - Configurable filters and linearization
   - Direct integration with modern control systems

2. **Analog Output** (Alternative)
   - ±10V voltage output
   - 10 kHz ±5 kHz frequency output
   - Compatible with traditional data acquisition systems

### Physical Specifications
- **Mounting:** Round shaft ends with standard coupling interface
- **Construction:** Compact rotating design
- **Compatibility:** Downward compatible with T21WN series
- **Environmental:** Industrial grade construction

### Advantages for Motor Testing
1. **High Accuracy:** 0.1% accuracy class ensures precise measurements
2. **Wide Speed Range:** 30,000 rpm maximum far exceeds motor capabilities  
3. **Digital Integration:** IO-Link provides rich data including temperature monitoring
4. **Bandwidth:** 1 kHz bandwidth captures dynamic torque variations
5. **Built-in Speed Measurement:** 512/1024 impulses per revolution
6. **Temperature Compensation:** Built-in temperature monitoring

## Alternative Sensors Considered

### HBK T210-5 Nm
- **Pros:** Higher resolution for lower torque measurements
- **Cons:** May not capture full peak torque (10.64 N⋅m)
- **Verdict:** Not recommended due to insufficient range

### FUTEK TRS Series
- **Torque Range:** 1-1000 N⋅m options available
- **Features:** Multiple outputs, encoder options
- **Status:** Detailed specifications not accessible
- **Consideration:** Viable alternative pending specification review

### ATI Multi-Axis Sensors
- **Type:** 6-axis force/torque sensors
- **Pros:** Measures all forces and torques simultaneously
- **Cons:** More complex, higher cost, may be over-specified
- **Verdict:** Consider for advanced testing requiring multi-axis data

## Sensor Integration Specifications

### Mechanical Interface
- **Input Shaft:** Connect to motor coupling/adapter
- **Output Shaft:** Connect to load brake or dynamometer
- **Alignment:** Critical for accuracy - use precision shaft couplings
- **Support:** Bearing support may be required for longer test durations

### Electrical Interface
- **Power Supply:** 24V DC typical (verify with sensor specifications) 
- **Signal Output:** IO-Link master module or analog input cards
- **Sampling Rate:** Minimum 1 kHz for dynamic testing
- **Data Logging:** Real-time logging of torque, speed, power, temperature

### Calibration Requirements
- **Initial Calibration:** Factory calibrated to 0.1% accuracy
- **Periodic Calibration:** Annual recalibration recommended
- **Traceability:** NIST/ISO traceable calibration certificates
- **Field Verification:** Regular zero-point and span checks

## Cost-Benefit Analysis

### HBK T210-10Nm
- **Estimated Cost:** $8,000-12,000 USD (approximate)
- **Benefits:** High accuracy, digital integration, comprehensive data
- **ROI:** Justified for precision motor development and testing

### Lower-Cost Alternatives
- **Industrial Sensors:** $2,000-5,000 range
- **Trade-offs:** Potentially lower accuracy, limited digital features
- **Application:** Suitable for basic torque verification testing

## Final Recommendation

**Selected Sensor:** HBK T210-10Nm with IO-Link output

**Justification:**
1. **Perfect Range Match:** 10 N⋅m covers peak motor torque with margin
2. **Superior Accuracy:** 0.1% accuracy ensures reliable test data
3. **Digital Integration:** IO-Link provides comprehensive process data
4. **Future-Proof:** High bandwidth and speed rating for advanced testing
5. **Industry Standard:** HBK reputation for precision measurement equipment

**Next Steps:**
1. Contact HBK for detailed quotation and technical specifications
2. Verify IO-Link master compatibility with data acquisition system
3. Design mechanical mounting interface for test bed integration
4. Plan calibration and maintenance procedures