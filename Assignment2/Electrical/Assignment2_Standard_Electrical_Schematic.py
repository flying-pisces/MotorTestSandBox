#!/usr/bin/env python3
"""
Assignment 2 - Standard Electrical Schematic
Professional electrical schematic following IEEE/IEC standards
for Nanotec DB87M01-S BLDC motor control system
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, Arc
import numpy as np

# Set up the drawing parameters for standard electrical schematic
fig, ax = plt.subplots(1, 1, figsize=(17, 11))  # A3 landscape format
ax.set_xlim(0, 170)
ax.set_ylim(0, 110)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('white')

# Standard electrical colors
WIRE_POWER_L1 = '#8B4513'    # Brown - L1 
WIRE_POWER_L2 = '#000000'    # Black - L2
WIRE_POWER_L3 = '#808080'    # Gray - L3  
WIRE_NEUTRAL = '#0000FF'     # Blue - Neutral
WIRE_GROUND = '#00FF00'      # Green/Yellow - Ground
WIRE_DC_POS = '#FF0000'      # Red - DC+
WIRE_DC_NEG = '#000000'      # Black - DC-
WIRE_CONTROL = '#8B008B'     # Purple - Control circuits
WIRE_SIGNAL = '#FF4500'      # Orange - Signal lines

def draw_wire(ax, points, color='black', width=1.2, style='-'):
    """Draw electrical wires using standard line styles"""
    if len(points) >= 2:
        for i in range(len(points)-1):
            ax.plot([points[i][0], points[i+1][0]], 
                   [points[i][1], points[i+1][1]], 
                   color=color, linewidth=width, linestyle=style)

def draw_junction_dot(ax, x, y, color='black'):
    """Draw standard electrical junction dot"""
    ax.plot(x, y, 'o', color=color, markersize=4, markerfacecolor=color)

def draw_terminal(ax, x, y, label, direction='up'):
    """Draw terminal with standard numbering"""
    ax.plot(x, y, 'ko', markersize=3)
    if direction == 'up':
        ax.text(x, y+1, label, ha='center', va='bottom', fontsize=7)
    elif direction == 'down':
        ax.text(x, y-1, label, ha='center', va='top', fontsize=7)
    elif direction == 'left':
        ax.text(x-1, y, label, ha='right', va='center', fontsize=7)
    elif direction == 'right':
        ax.text(x+1, y, label, ha='left', va='center', fontsize=7)

def draw_fuse(ax, x, y, width=6, label="F1", rating="10A"):
    """Draw standard fuse symbol"""
    # Fuse rectangle
    rect = Rectangle((x-width/2, y-1), width, 2, 
                    fill=False, edgecolor='black', linewidth=1.2)
    ax.add_patch(rect)
    
    # Connection lines
    ax.plot([x-width/2-3, x-width/2], [y, y], 'k-', linewidth=1.2)
    ax.plot([x+width/2, x+width/2+3], [y, y], 'k-', linewidth=1.2)
    
    # Label and rating
    ax.text(x, y-3, f"{label}\n{rating}", ha='center', va='top', fontsize=8, fontweight='bold')
    
    return (x-width/2-3, y), (x+width/2+3, y)

def draw_circuit_breaker(ax, x, y, width=8, label="Q1", rating="16A"):
    """Draw standard circuit breaker symbol"""
    # Main body
    rect = Rectangle((x-width/2, y-2), width, 4, 
                    fill=False, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    
    # Trip curve symbol
    ax.plot([x-1, x+1], [y-0.5, y+0.5], 'k-', linewidth=1.5)
    ax.text(x+2, y, 'B', ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Connection lines
    ax.plot([x-width/2-3, x-width/2], [y, y], 'k-', linewidth=1.2)
    ax.plot([x+width/2, x+width/2+3], [y, y], 'k-', linewidth=1.2)
    
    # Label
    ax.text(x, y-4, f"{label}\n{rating}", ha='center', va='top', fontsize=8, fontweight='bold')
    
    return (x-width/2-3, y), (x+width/2+3, y)

def draw_transformer_psu(ax, x, y, width=16, height=12, label="T1", 
                        primary="230V", secondary="48V/24V"):
    """Draw power supply with transformer symbol"""
    # Main enclosure
    rect = Rectangle((x-width/2, y-height/2), width, height, 
                    fill=True, facecolor='lightgray', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    
    # Transformer symbol - Primary
    primary_coil = Circle((x-4, y), 2, fill=False, edgecolor='black', linewidth=1.2)
    ax.add_patch(primary_coil)
    
    # Transformer symbol - Secondary  
    secondary_coil = Circle((x+4, y), 2, fill=False, edgecolor='black', linewidth=1.2)
    ax.add_patch(secondary_coil)
    
    # Core lines
    ax.plot([x-1, x-1], [y-4, y+4], 'k-', linewidth=2)
    ax.plot([x+1, x+1], [y-4, y+4], 'k-', linewidth=2)
    
    # Input terminals
    draw_terminal(ax, x-width/2-3, y+2, 'L', 'left')
    draw_terminal(ax, x-width/2-3, y-2, 'N', 'left')
    ax.plot([x-width/2-3, x-width/2], [y+2, y+2], 'k-', linewidth=1.2)
    ax.plot([x-width/2-3, x-width/2], [y-2, y-2], 'k-', linewidth=1.2)
    
    # Output terminals - 48V
    draw_terminal(ax, x+width/2+3, y+4, '+48V', 'right')
    draw_terminal(ax, x+width/2+3, y+2, 'GND', 'right')
    ax.plot([x+width/2, x+width/2+3], [y+4, y+4], 'k-', linewidth=1.2)
    ax.plot([x+width/2, x+width/2+3], [y+2, y+2], 'k-', linewidth=1.2)
    
    # Output terminals - 24V
    draw_terminal(ax, x+width/2+3, y-2, '+24V', 'right')
    draw_terminal(ax, x+width/2+3, y-4, 'GND', 'right')
    ax.plot([x+width/2, x+width/2+3], [y-2, y-2], 'k-', linewidth=1.2)
    ax.plot([x+width/2, x+width/2+3], [y-4, y-4], 'k-', linewidth=1.2)
    
    # Labels
    ax.text(x, y-height/2-2, f"{label}", ha='center', va='top', fontsize=10, fontweight='bold')
    ax.text(x-6, y+6, primary, ha='center', va='bottom', fontsize=8)
    ax.text(x+6, y+6, secondary, ha='center', va='bottom', fontsize=8)
    
    return {
        'input_L': (x-width/2-3, y+2),
        'input_N': (x-width/2-3, y-2),
        'output_48V': (x+width/2+3, y+4),
        'output_24V': (x+width/2+3, y-2),
        'output_GND': [(x+width/2+3, y+2), (x+width/2+3, y-4)]
    }

def draw_contactor(ax, x, y, width=8, height=12, label="K1", coil_voltage="24V"):
    """Draw standard contactor symbol (IEC)"""
    # Main coil
    coil_rect = Rectangle((x-width/2, y-height/2), width, 4, 
                         fill=False, edgecolor='black', linewidth=1.2)
    ax.add_patch(coil_rect)
    
    # Coil terminals
    draw_terminal(ax, x-2, y-height/2-3, 'A1', 'down')
    draw_terminal(ax, x+2, y-height/2-3, 'A2', 'down')
    ax.plot([x-2, x-2], [y-height/2-3, y-height/2], 'k-', linewidth=1.2)
    ax.plot([x+2, x+2], [y-height/2-3, y-height/2], 'k-', linewidth=1.2)
    
    # Main contacts (3 pole)
    contact_y = y + 2
    for i, phase in enumerate(['L1', 'L2', 'L3']):
        contact_x = x - 4 + i * 4
        
        # Fixed contact
        ax.plot([contact_x, contact_x], [contact_y+2, contact_y+4], 'k-', linewidth=2)
        # Moving contact
        ax.plot([contact_x-0.5, contact_x+0.5], [contact_y, contact_y], 'k-', linewidth=2)
        ax.plot([contact_x, contact_x], [contact_y-2, contact_y], 'k-', linewidth=1.2)
        
        # Terminal numbers
        draw_terminal(ax, contact_x, contact_y+4, f"{i+1}", 'up')
        draw_terminal(ax, contact_x, contact_y-2, f"{i+2}", 'down')
        
        # Phase labels
        ax.text(contact_x, contact_y+6, phase, ha='center', va='bottom', fontsize=7)
    
    # Label
    ax.text(x, y-height/2-5, f"{label}\n{coil_voltage}", ha='center', va='top', 
           fontsize=8, fontweight='bold')
    
    return {
        'coil_A1': (x-2, y-height/2-3),
        'coil_A2': (x+2, y-height/2-3),
        'contacts': [(x-4, contact_y+4), (x, contact_y+4), (x+4, contact_y+4)],
        'outputs': [(x-4, contact_y-2), (x, contact_y-2), (x+4, contact_y-2)]
    }

def draw_motor_symbol(ax, x, y, diameter=12, label="M1", motor_type="BLDC"):
    """Draw standard 3-phase motor symbol"""
    # Motor circle
    motor_circle = Circle((x, y), diameter/2, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(motor_circle)
    
    # Motor designation
    ax.text(x, y, 'M\n3~', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Terminal connections (120° apart)
    angles = [90, 210, 330]  # degrees
    terminals = []
    
    for i, angle in enumerate(angles):
        rad = np.radians(angle)
        term_x = x + (diameter/2 + 3) * np.cos(rad)
        term_y = y + (diameter/2 + 3) * np.sin(rad)
        
        ax.plot([x + diameter/2 * np.cos(rad), term_x], 
               [y + diameter/2 * np.sin(rad), term_y], 'k-', linewidth=1.5)
        
        terminals.append((term_x, term_y))
        
        # Terminal labels
        phase_labels = ['U', 'V', 'W']
        if angle == 90:  # top
            ax.text(term_x, term_y+2, phase_labels[i], ha='center', va='bottom', fontsize=8, fontweight='bold')
        elif angle == 210:  # bottom left
            ax.text(term_x-2, term_y, phase_labels[i], ha='right', va='center', fontsize=8, fontweight='bold')
        else:  # bottom right
            ax.text(term_x+2, term_y, phase_labels[i], ha='left', va='center', fontsize=8, fontweight='bold')
    
    # Motor label
    ax.text(x, y-diameter/2-4, f"{label}\n{motor_type}", ha='center', va='top', 
           fontsize=9, fontweight='bold')
    
    return terminals

def draw_encoder_symbol(ax, x, y, width=10, height=8, label="B1"):
    """Draw encoder sensor symbol"""
    # Main body
    rect = Rectangle((x-width/2, y-height/2), width, height, 
                    fill=True, facecolor='lightblue', edgecolor='black', linewidth=1.2)
    ax.add_patch(rect)
    
    # Encoder disk symbol
    disk = Circle((x, y), 2, fill=False, edgecolor='black', linewidth=1.2)
    ax.add_patch(disk)
    ax.plot([x-1, x+1], [y-1, y+1], 'k-', linewidth=1)
    ax.plot([x-1, x+1], [y+1, y-1], 'k-', linewidth=1)
    
    # Output terminals
    terminals = []
    for i, (pin, label_text) in enumerate([('1', '5V'), ('2', 'A'), ('3', 'B'), ('4', 'Z'), ('5', 'GND')]):
        term_x = x - 4 + i * 2
        term_y = y + height/2 + 3
        terminals.append((term_x, term_y))
        draw_terminal(ax, term_x, term_y, pin, 'up')
        ax.text(term_x, term_y+3, label_text, ha='center', va='bottom', fontsize=6)
    
    ax.text(x, y-height/2-2, f"{label}\n1000 PPR", ha='center', va='top', fontsize=8, fontweight='bold')
    
    return terminals

def draw_emergency_stop(ax, x, y, diameter=8, label="S0"):
    """Draw emergency stop button (mushroom type)"""
    # Button circle (red)
    button = Circle((x, y), diameter/2, fill=True, facecolor='red', 
                   edgecolor='black', linewidth=2)
    ax.add_patch(button)
    
    # NC contact symbol
    contact_y = y - diameter/2 - 4
    ax.plot([x-3, x-1], [contact_y, contact_y], 'k-', linewidth=2)
    ax.plot([x+1, x+3], [contact_y, contact_y], 'k-', linewidth=2)
    ax.plot([x-1, x+1], [contact_y+1, contact_y+1], 'k-', linewidth=2)
    
    # Connection to button
    ax.plot([x, x], [y-diameter/2, contact_y+1], 'k--', linewidth=1)
    
    # Terminal points
    draw_terminal(ax, x-3, contact_y, '11', 'down')
    draw_terminal(ax, x+3, contact_y, '12', 'down')
    
    ax.text(x, y-diameter/2-8, f"{label}\nE-STOP\nNC", ha='center', va='top', 
           fontsize=8, fontweight='bold')
    
    return (x-3, contact_y), (x+3, contact_y)

def draw_limit_switch(ax, x, y, label="S1", switch_type="NO"):
    """Draw limit switch symbol"""
    # Switch contacts
    if switch_type == "NO":
        ax.plot([x-3, x-1], [y, y], 'k-', linewidth=2)
        ax.plot([x+1, x+3], [y, y], 'k-', linewidth=2)
        ax.plot([x-1, x+0.5], [y+1, y], 'k-', linewidth=2)
    else:  # NC
        ax.plot([x-3, x-1], [y, y], 'k-', linewidth=2)
        ax.plot([x+1, x+3], [y, y], 'k-', linewidth=2)
        ax.plot([x-1, x+1], [y+1, y+1], 'k-', linewidth=2)
    
    # Actuator
    ax.plot([x, x], [y+1, y+3], 'k-', linewidth=1.5)
    ax.plot([x-1, x+1], [y+3, y+3], 'k-', linewidth=3)
    
    draw_terminal(ax, x-3, y, '1', 'down')
    draw_terminal(ax, x+3, y, '2', 'down')
    
    ax.text(x, y-3, f"{label}\n{switch_type}", ha='center', va='top', 
           fontsize=8, fontweight='bold')
    
    return (x-3, y), (x+3, y)

def draw_current_sensor(ax, x, y, width=8, height=6, label="CT1"):
    """Draw current transformer symbol"""
    # CT core
    ct_circle = Circle((x, y), 3, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(ct_circle)
    
    # Primary conductor (through center)
    ax.plot([x-4, x+4], [y, y], 'k-', linewidth=3)
    
    # Secondary winding
    ax.plot([x+1, x+3], [y-2, y-2], 'k-', linewidth=1.2)
    ax.plot([x+3, x+3], [y-2, y-4], 'k-', linewidth=1.2)
    
    # Output terminals
    draw_terminal(ax, x+3, y-4, '+', 'right')
    draw_terminal(ax, x-3, y-4, '-', 'left')
    
    ax.text(x, y-6, f"{label}\n50A:5A", ha='center', va='top', fontsize=8, fontweight='bold')
    
    return (x-4, y), (x+4, y), (x+3, y-4), (x-3, y-4)

def draw_safety_relay(ax, x, y, width=12, height=16, label="K1S"):
    """Draw safety relay symbol"""
    # Main body
    rect = Rectangle((x-width/2, y-height/2), width, height, 
                    fill=True, facecolor='yellow', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    
    # Safety symbol
    ax.text(x, y+2, '⚠', ha='center', va='center', fontsize=16)
    ax.text(x, y-2, 'SIL3', ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Input terminals
    draw_terminal(ax, x-4, y-height/2-3, '13', 'down')
    draw_terminal(ax, x-2, y-height/2-3, '14', 'down') 
    draw_terminal(ax, x+2, y-height/2-3, 'A1', 'down')
    draw_terminal(ax, x+4, y-height/2-3, 'A2', 'down')
    
    # Output terminals
    draw_terminal(ax, x-2, y+height/2+3, '13', 'up')
    draw_terminal(ax, x+2, y+height/2+3, '14', 'up')
    
    ax.text(x, y-height/2-5, f"{label}\nSafety Relay", ha='center', va='top', 
           fontsize=8, fontweight='bold')
    
    return {
        'input_13': (x-4, y-height/2-3),
        'input_14': (x-2, y-height/2-3),
        'coil_A1': (x+2, y-height/2-3),
        'coil_A2': (x+4, y-height/2-3),
        'output_13': (x-2, y+height/2+3),
        'output_14': (x+2, y+height/2+3)
    }

def draw_bldc_controller(ax, x, y, width=20, height=16, label="VFD1"):
    """Draw BLDC motor controller"""
    # Main enclosure
    rect = Rectangle((x-width/2, y-height/2), width, height, 
                    fill=True, facecolor='lightcyan', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    
    # Power electronics symbol
    ax.text(x, y+2, '≈', ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(x, y-2, 'BLDC', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # DC input terminals
    draw_terminal(ax, x-width/2-3, y+4, '+48V', 'left')
    draw_terminal(ax, x-width/2-3, y, 'GND', 'left')
    draw_terminal(ax, x-width/2-3, y-4, '+24V', 'left')
    
    # AC output terminals (3-phase)
    draw_terminal(ax, x+width/2+3, y+4, 'U', 'right')
    draw_terminal(ax, x+width/2+3, y, 'V', 'right')
    draw_terminal(ax, x+width/2+3, y-4, 'W', 'right')
    
    # Communication terminals
    draw_terminal(ax, x, y-height/2-3, 'A+', 'down')
    draw_terminal(ax, x+3, y-height/2-3, 'B-', 'down')
    draw_terminal(ax, x+6, y-height/2-3, 'GND', 'down')
    
    ax.text(x, y-height/2-5, f"{label}\nNanotec SMCI47-S\nBLDC Controller", 
           ha='center', va='top', fontsize=8, fontweight='bold')
    
    return {
        'dc_48v': (x-width/2-3, y+4),
        'dc_gnd': (x-width/2-3, y),
        'dc_24v': (x-width/2-3, y-4),
        'ac_u': (x+width/2+3, y+4),
        'ac_v': (x+width/2+3, y),
        'ac_w': (x+width/2+3, y-4),
        'comm_a': (x, y-height/2-3),
        'comm_b': (x+3, y-height/2-3),
        'comm_gnd': (x+6, y-height/2-3)
    }

def draw_microcontroller(ax, x, y, width=16, height=12, label="PLC1"):
    """Draw microcontroller/PLC"""
    # Main body
    rect = Rectangle((x-width/2, y-height/2), width, height, 
                    fill=True, facecolor='lightgreen', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    
    # CPU symbol
    ax.text(x, y, 'CPU', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Power terminals
    draw_terminal(ax, x-width/2-3, y+2, '+24V', 'left')
    draw_terminal(ax, x-width/2-3, y-2, 'GND', 'left')
    
    # Communication terminals
    draw_terminal(ax, x+width/2+3, y+2, 'A+', 'right')
    draw_terminal(ax, x+width/2+3, y, 'B-', 'right')
    draw_terminal(ax, x+width/2+3, y-2, 'GND', 'right')
    
    # Digital I/O
    draw_terminal(ax, x, y+height/2+3, 'DI1', 'up')
    draw_terminal(ax, x+3, y+height/2+3, 'DI2', 'up')
    
    ax.text(x, y-height/2-2, f"{label}\nArduino Mega", ha='center', va='top', 
           fontsize=8, fontweight='bold')
    
    return {
        'power_24v': (x-width/2-3, y+2),
        'power_gnd': (x-width/2-3, y-2),
        'comm_a': (x+width/2+3, y+2),
        'comm_b': (x+width/2+3, y),
        'comm_gnd': (x+width/2+3, y-2),
        'di1': (x, y+height/2+3),
        'di2': (x+3, y+height/2+3)
    }

print("🔌 Creating Standard Electrical Schematic...")
print("Following IEEE/IEC electrical drawing standards")

# Create the main schematic following standard practices

# Title block (bottom right corner)
title_x, title_y = 120, 10
title_rect = Rectangle((title_x, title_y), 45, 20, 
                      fill=True, facecolor='lightgray', 
                      edgecolor='black', linewidth=1.5)
ax.add_patch(title_rect)

ax.text(title_x + 22.5, title_y + 16, 'ASSIGNMENT 2 - ELECTRICAL SCHEMATIC', 
       ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(title_x + 22.5, title_y + 13, 'Pendulum Testbed Control System', 
       ha='center', va='center', fontsize=10)
ax.text(title_x + 22.5, title_y + 10, 'Motor: Nanotec DB87M01-S BLDC', 
       ha='center', va='center', fontsize=9)
ax.text(title_x + 2, title_y + 6, 'Drawn by: Claude AI', ha='left', va='center', fontsize=8)
ax.text(title_x + 2, title_y + 4, 'Date: August 2025', ha='left', va='center', fontsize=8)
ax.text(title_x + 2, title_y + 2, 'Standard: IEEE 315/IEC 60617', ha='left', va='center', fontsize=8)

# AC Power Input (top left)
print("  ⚡ Drawing AC power input...")
ax.text(15, 100, '230V AC\n50Hz', ha='center', va='center', fontsize=10, fontweight='bold',
       bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue'))

# Main circuit breaker
q1_in, q1_out = draw_circuit_breaker(ax, 15, 95, label="Q1", rating="16A B")

# Power supply
psu_connections = draw_transformer_psu(ax, 40, 85, label="PSU1")

# Connect AC input to PSU
draw_wire(ax, [(15, 97), (psu_connections['input_L'])], WIRE_POWER_L1, width=2)
draw_wire(ax, [(15, 93), (psu_connections['input_N'])], WIRE_NEUTRAL, width=2)

# Safety relay
print("  🛡️  Drawing safety system...")
safety_relay = draw_safety_relay(ax, 90, 85, label="K1S")

# Emergency stop
estop_11, estop_12 = draw_emergency_stop(ax, 70, 95, label="S0")

# Limit switches  
limit1_1, limit1_2 = draw_limit_switch(ax, 70, 80, label="S1", switch_type="NO")
limit2_1, limit2_2 = draw_limit_switch(ax, 70, 65, label="S2", switch_type="NO") 

# Connect safety circuit
draw_wire(ax, [psu_connections['output_24V'], (65, 87), estop_11], WIRE_DC_POS, width=1.5)
draw_wire(ax, [estop_12, safety_relay['input_13']], WIRE_CONTROL, width=1.5)
draw_wire(ax, [safety_relay['input_14'], limit1_1], WIRE_CONTROL, width=1.5)
draw_wire(ax, [limit1_2, limit2_1], WIRE_CONTROL, width=1.5)

# Main controller
print("  💻 Drawing control system...")
controller = draw_microcontroller(ax, 110, 85, label="PLC1")

# Connect controller power
draw_wire(ax, [safety_relay['output_13'], controller['power_24v']], WIRE_DC_POS, width=1.5)

# BLDC Controller  
print("  🎛️  Drawing BLDC controller...")
bldc_ctrl = draw_bldc_controller(ax, 40, 50, label="VFD1")

# Connect DC power to BLDC controller
draw_wire(ax, [psu_connections['output_48V'], bldc_ctrl['dc_48v']], WIRE_DC_POS, width=2)
draw_wire(ax, [psu_connections['output_24V'], bldc_ctrl['dc_24v']], WIRE_DC_POS, width=1.5)

# Motor
print("  🔧 Drawing BLDC motor...")
motor_terminals = draw_motor_symbol(ax, 100, 50, label="M1", motor_type="BLDC\nDB87M01-S")

# Connect motor power (3-phase)
draw_wire(ax, [bldc_ctrl['ac_u'], motor_terminals[0]], WIRE_POWER_L1, width=2)
draw_wire(ax, [bldc_ctrl['ac_v'], motor_terminals[1]], WIRE_POWER_L2, width=2)  
draw_wire(ax, [bldc_ctrl['ac_w'], motor_terminals[2]], WIRE_POWER_L3, width=2)

# Encoder
print("  📍 Drawing encoder...")
encoder_terminals = draw_encoder_symbol(ax, 100, 30, label="B1")

# Current sensor
print("  📊 Drawing current sensor...")
ct1_in, ct2_out, ct_pos, ct_neg = draw_current_sensor(ax, 70, 50, label="CT1")

# RS485 Communication network
print("  🔗 Drawing communication network...")
# Communication bus between controller and BLDC drive
draw_wire(ax, [controller['comm_a'], bldc_ctrl['comm_a']], WIRE_SIGNAL, width=1, style='--')
draw_wire(ax, [controller['comm_b'], bldc_ctrl['comm_b']], WIRE_SIGNAL, width=1, style='--')

# Ground/common connections
print("  ⏚  Drawing ground connections...")
ground_points = [
    psu_connections['output_GND'][0], psu_connections['output_GND'][1],
    bldc_ctrl['dc_gnd'], controller['power_gnd'], 
    safety_relay['coil_A2'], bldc_ctrl['comm_gnd']
]

# Draw ground symbols and connections
for gnd_point in ground_points:
    # Ground symbol
    ax.plot([gnd_point[0], gnd_point[0]], [gnd_point[1], gnd_point[1]-2], 'k-', linewidth=1.5)
    ax.plot([gnd_point[0]-1, gnd_point[0]+1], [gnd_point[1]-2, gnd_point[1]-2], 'k-', linewidth=2)
    ax.plot([gnd_point[0]-0.5, gnd_point[0]+0.5], [gnd_point[1]-2.5, gnd_point[1]-2.5], 'k-', linewidth=1.5)
    ax.plot([gnd_point[0]-0.2, gnd_point[0]+0.2], [gnd_point[1]-3, gnd_point[1]-3], 'k-', linewidth=1)

# Wire labels and ratings
print("  🏷️  Adding wire labels...")
ax.text(25, 97, 'L1\n16A', ha='center', va='bottom', fontsize=7, 
       bbox=dict(boxstyle="round,pad=0.1", facecolor='white'))
ax.text(50, 77, '48V DC\n10A', ha='center', va='bottom', fontsize=7,
       bbox=dict(boxstyle="round,pad=0.1", facecolor='white'))
ax.text(80, 52, 'U1', ha='center', va='bottom', fontsize=7, rotation=15)
ax.text(85, 48, 'V1', ha='center', va='bottom', fontsize=7, rotation=0)
ax.text(80, 44, 'W1', ha='center', va='bottom', fontsize=7, rotation=-15)

# Circuit reference designations
circuit_refs = [
    (15, 105, "Circuit: Main AC Input"),
    (40, 105, "Circuit: Power Supply"),  
    (90, 105, "Circuit: Safety System"),
    (110, 105, "Circuit: Control System"),
    (40, 35, "Circuit: Motor Drive"),
    (100, 20, "Circuit: Feedback System")
]

for x, y, ref in circuit_refs:
    ax.text(x, y, ref, ha='center', va='center', fontsize=8, 
           bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow', alpha=0.7))

# Component list (left side)
print("  📋 Adding component list...")
comp_list_x = 5
comp_list_y = 70

components = [
    "Q1 - Circuit Breaker 16A B-Type",
    "PSU1 - Power Supply 230V/48V-24V", 
    "K1S - Safety Relay SIL3",
    "S0 - Emergency Stop NC",
    "S1,S2 - Limit Switches NO",
    "PLC1 - Arduino Mega Controller",
    "VFD1 - BLDC Controller SMCI47-S",
    "M1 - Motor DB87M01-S 48V 440W",
    "B1 - Encoder 1000 PPR",
    "CT1 - Current Transformer 50A:5A"
]

ax.text(comp_list_x, comp_list_y + 5, 'COMPONENT LIST:', 
       fontsize=10, fontweight='bold')

for i, comp in enumerate(components):
    ax.text(comp_list_x, comp_list_y - i*2, f"• {comp}", fontsize=8)

# Legend (bottom left)
legend_x = 5
legend_y = 35
ax.text(legend_x, legend_y, 'WIRE LEGEND:', fontsize=10, fontweight='bold')

wire_legend = [
    (WIRE_POWER_L1, 'AC L1 (Brown)', 2),
    (WIRE_NEUTRAL, 'Neutral (Blue)', 2),
    (WIRE_DC_POS, 'DC+ (Red)', 1.5),
    (WIRE_DC_NEG, 'DC- (Black)', 1.5), 
    (WIRE_CONTROL, 'Control (Purple)', 1),
    (WIRE_SIGNAL, 'RS485 (Orange)', 1)
]

for i, (color, label, width) in enumerate(wire_legend):
    y_pos = legend_y - 2 - i*2
    ax.plot([legend_x, legend_x+3], [y_pos, y_pos], 
           color=color, linewidth=width, linestyle='--' if 'RS485' in label else '-')
    ax.text(legend_x+4, y_pos, label, fontsize=8, va='center')

plt.tight_layout()

# Save the schematic
output_file = '/Users/cyin/project/robot/MotorTestSandBox/Assignment2/Electrical/Assignment2_Standard_Electrical_Schematic.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')

print(f"✅ Standard electrical schematic saved to: {output_file}")
print("📐 Schematic follows IEEE/IEC standards with:")
print("   • Proper electrical symbols and designations")
print("   • Standard wire colors and ratings")  
print("   • Component reference designations")
print("   • Title block and documentation")
print("   • Professional electrical layout")

# plt.show()  # Commented for batch execution