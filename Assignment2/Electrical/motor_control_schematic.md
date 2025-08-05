# Assignment 2: Electrical Control System Design

## Motor Specifications
- **Selected Motor:** Nanotec DB87M01-S
- **Motor Type:** Stepper motor with integrated controller
- **URL:** https://en.nanotec.com/products/650-db87m01-s

## System Requirements
- **Control Type:** Position controlled
- **Motion Profile:** Continuous cycling between 0° and 90° 
- **Load:** 2kg pendulum at 0.3m radius
- **Required Motor Torque:** 0.3924 N⋅m (calculated)

## Electrical Schematic Components

### Main Components:
1. **Power Supply**
   - 24V DC supply (typical for Nanotec steppers)
   - Minimum 5A capacity for safety margin
   - Model: Mean Well LRS-150-24

2. **Motor Controller/Driver**
   - Integrated in DB87M01-S motor
   - Built-in controller with CANopen, Modbus, or RS485 interface

3. **Main Controller**
   - Arduino Uno R3 or similar microcontroller
   - USB programming interface
   - Digital I/O for motor communication

4. **Position Feedback**
   - Encoder integrated in motor (if available)
   - Alternative: External rotary encoder on output shaft
   - Model: Bourns EMS22A50-B28-LS6 (absolute encoder)

5. **Safety Components**
   - Emergency stop button (NC contacts)
   - Limit switches at 0° and 90° positions
   - Power indicator LED
   - Motor enable switch

### Wiring Diagram:

```
[24V PSU] ────┬─── [Motor Power Input]
              │
              └─── [Arduino VIN] (through 7812 regulator)

[Arduino] ──── RS485/Modbus ──── [Motor Controller]

[E-Stop] ──── NC contacts ──── [Safety Relay] ──── [Motor Enable]

[Limit SW 0°] ──── [Arduino D2]
[Limit SW 90°] ─── [Arduino D3]
[Enable Button] ── [Arduino D4]
[Position Encoder] [Arduino A0-A1] (if external)
```

## Control Interface Options

### Option 1: RS485/Modbus Communication
```
Arduino ←→ MAX485 Module ←→ Motor Controller
- Simple 2-wire communication
- Standard Modbus protocol
- Position commands via register writes
```

### Option 2: CANopen Interface
```
Arduino + MCP2515 ←→ CAN Bus ←→ Motor Controller
- More robust for industrial applications
- Higher data rates
- Better error handling
```

### Option 3: Analog Control (if supported)
```
Arduino PWM ←→ 0-10V Converter ←→ Motor Analog Input
- Simple speed/position control
- Less precise than digital
- Backup option
```

## Component List

| Component | Part Number | Quantity | Purpose |
|-----------|------------|----------|---------|
| Stepper Motor | Nanotec DB87M01-S | 1 | Main drive motor |
| Power Supply | Mean Well LRS-150-24 | 1 | 24V motor power |
| Microcontroller | Arduino Uno R3 | 1 | Main controller |
| RS485 Module | MAX485 | 1 | Motor communication |
| E-Stop Button | Schneider XB4BS8445 | 1 | Safety |
| Limit Switches | Omron D4V-8108Z | 2 | Position limits |
| Safety Relay | Pilz PNOZ s3 | 1 | Safety circuit |
| Enclosure | Hammond 1411N | 1 | Protection |
| Terminal Blocks | Phoenix Contact | Various | Connections |

## Safety Features

1. **Emergency Stop Circuit**
   - Hardwired E-stop button
   - Immediately cuts motor power
   - Requires manual reset

2. **Limit Switches**
   - Physical stops at 0° and 90°
   - Software limits with hardware backup
   - Prevents mechanical damage

3. **Software Watchdog**
   - Motor timeout protection
   - Communication loss detection
   - Automatic safe state entry

4. **Power Monitoring**
   - Voltage monitoring
   - Overcurrent protection
   - Temperature monitoring (if available)

## Control Software Requirements

The C++ control script must implement:
- Position feedback loop
- Smooth acceleration/deceleration profiles
- Safety interlocks
- Error handling and recovery
- Data logging capabilities

## Installation Notes

1. **Grounding:** Ensure proper grounding of all components
2. **Cable Shielding:** Use shielded cables for encoder signals
3. **Power Separation:** Separate digital and motor power supplies
4. **Ventilation:** Ensure adequate cooling for motor and drives
5. **Vibration:** Mount components to minimize vibration effects

## Testing and Commissioning

1. **Power-on Test:** Verify all voltages and connections
2. **Communication Test:** Confirm motor controller communication
3. **Safety Test:** Verify E-stop and limit switches
4. **Motion Test:** Test basic positioning commands
5. **Load Test:** Full operation with pendulum load
6. **Endurance Test:** Extended cycling for reliability verification