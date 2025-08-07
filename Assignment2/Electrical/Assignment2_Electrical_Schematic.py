#!/usr/bin/env python3
"""
Assignment 2 Electrical Schematic - Pendulum Testbed
Creates detailed electrical schematic for Nanotec DB87M01-S BLDC motor control
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the drawing parameters
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 100)
ax.set_ylim(0, 80)
ax.set_aspect('equal')
ax.axis('off')

# Colors for different component types
COLOR_POWER = '#FF6B6B'      # Red - Power supply
COLOR_CONTROL = '#4ECDC4'    # Teal - Control components
COLOR_MOTOR = '#45B7D1'      # Blue - Motor components
COLOR_SAFETY = '#FFA726'     # Orange - Safety components
COLOR_FEEDBACK = '#66BB6A'   # Green - Feedback/sensors
COLOR_WIRE_POWER = '#FF4444'  # Red wires - Power
COLOR_WIRE_SIGNAL = '#4444FF' # Blue wires - Signal
COLOR_WIRE_SAFETY = '#FF8800' # Orange wires - Safety

def draw_component_box(ax, x, y, width, height, color, label, sublabel="", 
                      terminals=None, pin_labels=None):
    """Draw a component box with terminals"""
    
    # Main component box
    box = FancyBboxPatch((x, y), width, height,
                        boxstyle="round,pad=0.3",
                        facecolor=color,
                        edgecolor='black',
                        linewidth=1.5,
                        alpha=0.8)
    ax.add_patch(box)
    
    # Component label
    ax.text(x + width/2, y + height/2 + 1, label, 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Component sublabel
    if sublabel:
        ax.text(x + width/2, y + height/2 - 1, sublabel, 
                ha='center', va='center', fontsize=8)
    
    # Draw terminals if specified
    if terminals:
        terminal_spacing = width / (len(terminals) + 1)
        for i, (term_label, term_type) in enumerate(terminals):
            term_x = x + (i + 1) * terminal_spacing
            
            if term_type == 'input':
                term_y = y - 1
                ax.plot(term_x, term_y, 'ko', markersize=4)
                ax.plot([term_x, term_x], [term_y, y], 'k-', linewidth=1)
            elif term_type == 'output':
                term_y = y + height + 1
                ax.plot(term_x, term_y, 'ko', markersize=4)
                ax.plot([term_x, term_x], [y + height, term_y], 'k-', linewidth=1)
            
            # Terminal label
            if pin_labels and i < len(pin_labels):
                offset_y = -2 if term_type == 'input' else 2
                ax.text(term_x, term_y + offset_y, pin_labels[i], 
                       ha='center', va='center', fontsize=7)

def draw_wire(ax, start, end, color=COLOR_WIRE_SIGNAL, style='-', width=2, label=""):
    """Draw a wire connection between two points"""
    
    x1, y1 = start
    x2, y2 = end
    
    # Draw the wire
    ax.plot([x1, x2], [y1, y2], color=color, linestyle=style, linewidth=width)
    
    # Add voltage/current label if specified
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x, mid_y + 1, label, ha='center', va='center', 
               fontsize=7, bbox=dict(boxstyle="round,pad=0.2", 
               facecolor='white', alpha=0.8))

def draw_title_block(ax):
    """Draw title block with project information"""
    
    title_box = Rectangle((75, 2), 23, 15, 
                         facecolor='lightgray', 
                         edgecolor='black', 
                         linewidth=1.5)
    ax.add_patch(title_box)
    
    # Title text
    ax.text(86.5, 14, 'ASSIGNMENT 2', ha='center', va='center', 
           fontsize=14, fontweight='bold')
    ax.text(86.5, 12, 'Pendulum Testbed', ha='center', va='center', 
           fontsize=12)
    ax.text(86.5, 10, 'Electrical Schematic', ha='center', va='center', 
           fontsize=11)
    
    # Details
    ax.text(76, 8, 'Motor:', ha='left', va='center', fontsize=9, fontweight='bold')
    ax.text(76, 7, 'Nanotec DB87M01-S', ha='left', va='center', fontsize=8)
    ax.text(76, 6, 'BLDC 48V 440W', ha='left', va='center', fontsize=8)
    
    ax.text(76, 4.5, 'Control:', ha='left', va='center', fontsize=9, fontweight='bold')
    ax.text(76, 3.5, 'Position Control', ha='left', va='center', fontsize=8)
    ax.text(76, 2.5, '0° to 90° Motion', ha='left', va='center', fontsize=8)

# Create the electrical schematic drawing

print("🔌 Creating Assignment 2 Electrical Schematic...")
print("Motor: Nanotec DB87M01-S BLDC Motor (48V, 440W)")

# 1. POWER SUPPLY SECTION
print("  ⚡ Adding power supply components...")

# Main AC Input
ax.text(5, 75, '230V AC\nMains Input', ha='center', va='center', 
       fontsize=10, fontweight='bold',
       bbox=dict(boxstyle="round,pad=0.5", facecolor=COLOR_POWER, alpha=0.7))

# Circuit breaker
draw_component_box(ax, 2, 68, 6, 4, COLOR_POWER, 'MCB', '10A B-Type',
                  terminals=[('L', 'input'), ('N', 'input'), ('L', 'output'), ('N', 'output')],
                  pin_labels=['L', 'N', 'L', 'N'])

# 48V DC Power Supply for motor
draw_component_box(ax, 15, 68, 12, 6, COLOR_POWER, '48V DC PSU', 
                  'Mean Well RSP-320-48\n48V 6.7A 320W',
                  terminals=[('AC L', 'input'), ('AC N', 'input'), 
                           ('+48V', 'output'), ('-48V/GND', 'output')],
                  pin_labels=['L', 'N', '+48V', 'GND'])

# 24V DC Power Supply for control
draw_component_box(ax, 30, 68, 12, 6, COLOR_POWER, '24V DC PSU',
                  'Mean Well MW-RSD-100\n24V 4.2A 100W',
                  terminals=[('AC L', 'input'), ('AC N', 'input'),
                           ('+24V', 'output'), ('-24V/GND', 'output')],
                  pin_labels=['L', 'N', '+24V', 'GND'])

# 2. MOTOR CONTROLLER SECTION  
print("  🎛️  Adding motor controller...")

# BLDC Motor Controller
draw_component_box(ax, 15, 55, 15, 8, COLOR_CONTROL, 'BLDC Controller',
                  'Nanotec SMCI47-S\nBLDC Servo Controller\nRS485 Interface',
                  terminals=[('48V+', 'input'), ('GND', 'input'), 
                           ('24V+', 'input'), ('COM', 'input'),
                           ('U', 'output'), ('V', 'output'), ('W', 'output'),
                           ('A+', 'output'), ('B-', 'output')],
                  pin_labels=['48V+', 'GND', '24V+', 'COM', 
                            'U', 'V', 'W', 'A+', 'B-'])

# 3. MAIN MOTOR SECTION
print("  🔧 Adding Nanotec DB87M01-S motor...")

# DB87M01-S BLDC Motor
draw_component_box(ax, 45, 55, 18, 8, COLOR_MOTOR, 'DB87M01-S',
                  'Nanotec BLDC Motor\n48V 440W 3000rpm\n14.28 kgf·cm Rated Torque',
                  terminals=[('U', 'input'), ('V', 'input'), ('W', 'input'),
                           ('5V+', 'input'), ('A', 'output'), ('B', 'output'), 
                           ('Z', 'output'), ('GND', 'output')],
                  pin_labels=['U', 'V', 'W', '5V+', 'A', 'B', 'Z', 'GND'])

# 4. ENCODER SECTION
print("  📍 Adding encoder interface...")

# WEDS5541-B06 Encoder (integrated with motor)
draw_component_box(ax, 68, 55, 12, 8, COLOR_FEEDBACK, 'WEDS5541-B06',
                  '3Ch Incremental\nEncoder 5V\n1000 Lines/Rev',
                  terminals=[('5V+', 'input'), ('GND', 'input'),
                           ('A', 'output'), ('B', 'output'), ('Z', 'output')],
                  pin_labels=['5V+', 'GND', 'A', 'B', 'Z'])

# 5. CONTROL SYSTEM
print("  💻 Adding control system...")

# Main Controller - Arduino/Industrial PLC
draw_component_box(ax, 15, 40, 15, 8, COLOR_CONTROL, 'Main Controller',
                  'Arduino Mega 2560\nRS485 Shield\nMotion Control',
                  terminals=[('24V+', 'input'), ('GND', 'input'),
                           ('A+', 'output'), ('B-', 'output'),
                           ('5V+', 'output'), ('GND', 'output')],
                  pin_labels=['24V+', 'GND', 'A+', 'B-', '5V', 'GND'])

# HMI/Display
draw_component_box(ax, 35, 40, 12, 8, COLOR_CONTROL, 'HMI Display',
                  '7" Touch Panel\n24V Operation\nPosition Monitor',
                  terminals=[('24V+', 'input'), ('GND', 'input'),
                           ('RS485+', 'input'), ('RS485-', 'input')],
                  pin_labels=['24V+', 'GND', 'A+', 'B-'])

# 6. SAFETY SYSTEM
print("  🛡️  Adding safety components...")

# Emergency Stop Button
draw_component_box(ax, 5, 25, 8, 6, COLOR_SAFETY, 'Emergency Stop',
                  'Schneider XB5AS8425\n40mm Red Mushroom\nNC Contacts',
                  terminals=[('13', 'output'), ('14', 'output')],
                  pin_labels=['13', '14'])

# Safety Relay
draw_component_box(ax, 18, 25, 12, 6, COLOR_SAFETY, 'Safety Relay',
                  'Pilz PNOZ s30\nCategory 4 Safety\n24V Coil',
                  terminals=[('24V+', 'input'), ('GND', 'input'),
                           ('13', 'input'), ('14', 'input'),
                           ('13', 'output'), ('14', 'output')],
                  pin_labels=['A1', 'A2', '13', '14', '13', '14'])

# Position Limit Switches
draw_component_box(ax, 35, 25, 10, 6, COLOR_SAFETY, 'Limit Switches',
                  'Omron HL-5000\n0° and 90° Position\nNO/NC Contacts',
                  terminals=[('COM', 'input'), ('NO1', 'output'), ('NC1', 'output'),
                           ('COM', 'input'), ('NO2', 'output'), ('NC2', 'output')],
                  pin_labels=['C1', '1', '2', 'C2', '3', '4'])

# 7. FEEDBACK AND MONITORING
print("  📊 Adding monitoring systems...")

# Current Monitor
draw_component_box(ax, 50, 25, 12, 6, COLOR_FEEDBACK, 'Current Monitor',
                  'LEM HAL 50-S\nHall Effect Sensor\n±50A Range',
                  terminals=[('15V+', 'input'), ('GND', 'input'), ('OUT', 'output')],
                  pin_labels=['+15V', 'GND', 'Vout'])

# Position Encoder Display
draw_component_box(ax, 65, 25, 12, 6, COLOR_FEEDBACK, 'Position Display',
                  'Digital Counter\nLivestock LEE-6\nEncoder Input',
                  terminals=[('24V+', 'input'), ('GND', 'input'),
                           ('A+', 'input'), ('B-', 'input'), ('Z', 'input')],
                  pin_labels=['24V+', 'GND', 'A+', 'B-', 'Z'])

# 8. WIRE CONNECTIONS
print("  🔌 Drawing wire connections...")

# Power connections - 48V
draw_wire(ax, (8, 70), (15, 70), COLOR_WIRE_POWER, width=3, label='230V AC')
draw_wire(ax, (27, 70), (15, 57), COLOR_WIRE_POWER, width=3, label='48V DC')
draw_wire(ax, (30, 57), (45, 57), COLOR_WIRE_POWER, width=3, label='48V')

# Power connections - 24V  
draw_wire(ax, (36, 70), (18, 42), COLOR_WIRE_POWER, width=2, label='24V DC')
draw_wire(ax, (30, 42), (35, 42), COLOR_WIRE_POWER, width=2)

# Motor power connections (3-phase)
draw_wire(ax, (22.5, 63), (48, 63), COLOR_WIRE_POWER, width=4, label='U')
draw_wire(ax, (25, 63), (51, 63), COLOR_WIRE_POWER, width=4, label='V') 
draw_wire(ax, (27.5, 63), (54, 63), COLOR_WIRE_POWER, width=4, label='W')

# RS485 Communication
draw_wire(ax, (22.5, 55), (22.5, 48), COLOR_WIRE_SIGNAL, style='--', label='RS485')
draw_wire(ax, (41, 44), (35, 44), COLOR_WIRE_SIGNAL, style='--')

# Encoder signals
draw_wire(ax, (63, 59), (68, 59), COLOR_WIRE_SIGNAL, label='5V+')
draw_wire(ax, (57, 59), (74, 59), COLOR_WIRE_SIGNAL, label='A,B,Z')
draw_wire(ax, (30, 44), (74, 59), COLOR_WIRE_SIGNAL, style=':', label='Encoder')

# Safety circuit
draw_wire(ax, (9, 28), (18, 28), COLOR_WIRE_SAFETY, width=3, label='E-Stop')
draw_wire(ax, (30, 28), (35, 28), COLOR_WIRE_SAFETY, width=2, label='Safety OK')

# Limit switch connections  
draw_wire(ax, (40, 31), (40, 55), COLOR_WIRE_SAFETY, style=':', label='Limits')

# 9. COMPONENT SPECIFICATIONS TABLE
print("  📋 Adding component specifications...")

# Create specification table
spec_x, spec_y = 2, 2
spec_width, spec_height = 70, 15

spec_box = Rectangle((spec_x, spec_y), spec_width, spec_height,
                    facecolor='lightblue', alpha=0.3,
                    edgecolor='black', linewidth=1)
ax.add_patch(spec_box)

ax.text(spec_x + 1, spec_y + spec_height - 2, 'COMPONENT SPECIFICATIONS', 
       fontsize=12, fontweight='bold')

# Specifications text
specs = [
    "MOTOR: Nanotec DB87M01-S - BLDC Motor, 48V DC, 440W, 14.28 kgf·cm, 3000 rpm, NEMA 34",
    "ENCODER: WEDS5541-B06 - 3-Channel Incremental, 1000 lines/rev, 5V logic, Hall sensors",
    "CONTROLLER: Nanotec SMCI47-S - Servo Controller, RS485/Modbus interface, Position/Velocity control",
    "POWER: Mean Well RSP-320-48 (48V 6.7A) + RSD-100 (24V 4.2A) - Industrial PSU modules", 
    "SAFETY: Pilz PNOZ s30 Safety Relay + Schneider XB5AS8425 E-Stop - Category 4 SIL 3",
    "FEEDBACK: LEM HAL 50-S Current Sensor + Omron HL-5000 Limit Switches - Industrial grade",
    "CONTROL: Arduino Mega 2560 + RS485 Shield - Open source motion control platform",
    "HMI: 7-inch Industrial Touch Panel - 24V operation, RS485 communication interface"
]

for i, spec in enumerate(specs):
    ax.text(spec_x + 1, spec_y + spec_height - 4 - i*1.5, f"• {spec}", 
           fontsize=8, va='top')

# 10. WIRING DIAGRAM LEGEND
print("  🔍 Adding legend...")

legend_x, legend_y = 2, 50
legend_box = Rectangle((legend_x, legend_y), 10, 15,
                      facecolor='lightyellow', alpha=0.5,
                      edgecolor='black', linewidth=1)
ax.add_patch(legend_box)

ax.text(legend_x + 5, legend_y + 14, 'LEGEND', ha='center', fontweight='bold')

# Legend items
legend_items = [
    (COLOR_WIRE_POWER, '48V/230V Power', 4),
    (COLOR_WIRE_SIGNAL, 'Control Signal', 2),  
    (COLOR_WIRE_SAFETY, 'Safety Circuit', 3),
    ('black', 'Ground/Common', 1),
]

for i, (color, label, width) in enumerate(legend_items):
    y_pos = legend_y + 11 - i*2
    ax.plot([legend_x + 1, legend_x + 3], [y_pos, y_pos], 
           color=color, linewidth=width)
    ax.text(legend_x + 3.5, y_pos, label, fontsize=8, va='center')

# Signal types
ax.plot([legend_x + 1, legend_x + 3], [legend_y + 3, legend_y + 3], 
       'k--', linewidth=2)
ax.text(legend_x + 3.5, legend_y + 3, 'RS485 Comm', fontsize=8, va='center')

ax.plot([legend_x + 1, legend_x + 3], [legend_y + 1, legend_y + 1], 
       'k:', linewidth=2)
ax.text(legend_x + 3.5, legend_y + 1, 'Encoder/Sensor', fontsize=8, va='center')

# Draw title block
draw_title_block(ax)

# 11. SYSTEM OPERATION NOTES
notes_x, notes_y = 50, 2
notes_box = Rectangle((notes_x, notes_y), 23, 15,
                     facecolor='lightgreen', alpha=0.3,
                     edgecolor='black', linewidth=1)
ax.add_patch(notes_box)

ax.text(notes_x + 1, notes_y + 14, 'SYSTEM OPERATION', fontsize=10, fontweight='bold')

operation_notes = [
    "1. Position Control Mode:",
    "   • Target: 0° to 90° pendulum motion",
    "   • Feedback: 1000 line encoder",
    "   • Resolution: 0.36° per step",
    "",
    "2. Safety Features:",
    "   • Hardware E-stop circuit",
    "   • Dual limit switches at end positions", 
    "   • Current monitoring and protection",
    "",
    "3. Communication:",
    "   • RS485 Modbus for motor control",
    "   • Real-time position feedback",
    "   • HMI for operator interface"
]

for i, note in enumerate(operation_notes):
    ax.text(notes_x + 1, notes_y + 12 - i*0.8, note, fontsize=7, va='top')

plt.title('Assignment 2: Pendulum Testbed Electrical Schematic\nNanotec DB87M01-S BLDC Motor Control System', 
         fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()

# Save the schematic
output_file = '/Users/cyin/project/robot/MotorTestSandBox/Assignment2/Electrical/Assignment2_Electrical_Schematic.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')

print(f"✅ Electrical schematic saved to: {output_file}")
print("📐 Schematic includes:")
print("   • Complete power distribution (230V AC → 48V/24V DC)")
print("   • BLDC motor control with RS485 interface")
print("   • 1000-line encoder feedback system")
print("   • Category 4 safety system with E-stop")
print("   • Position limit switches and current monitoring")
print("   • Professional component specifications")

# plt.show()  # Commented out for batch execution

print(f"Schematic drawing completed successfully!")