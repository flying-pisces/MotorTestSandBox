#!/usr/bin/env python3
"""
Simple verification of Assignment 2 calculations
Working from first principles
"""

# System parameters
M = 2.0  # kg
L = 0.3  # m
g = 9.81  # m/s²

# Shaft diameters (mm)
Da = 20
Db = 30
Dc = 40
Dd = 50
De = 65

# Gearbox ratio
gear_ratio = 10

print("="*60)
print("SIMPLE VERIFICATION - Assignment 2")
print("="*60)

# 1. Pendulum torque (load)
T_pendulum = M * g * L
print(f"1. Pendulum torque: {T_pendulum:.4f} N⋅m")

# 2. Calculate total mechanical advantage
# Each rope stage provides diameter ratio advantage
rope_advantage = (De/Dd) * (Dd/Dc) * (Dc/Db) * (Db/Da)
total_advantage = rope_advantage * gear_ratio

print(f"2. Rope mechanical advantage: {rope_advantage:.2f}")
print(f"3. Total mechanical advantage: {total_advantage:.2f}")

# 3. Motor torque required
T_motor = T_pendulum / total_advantage
print(f"4. Motor torque required: {T_motor:.4f} N⋅m")

# 4. Working forward to verify forces
print(f"\n5. Force calculations (working backwards from load):")

# Force at shaft E (from pendulum torque)
F_de = (2 * T_pendulum) / (De/1000)  # Convert mm to m
print(f"   F_de = 2 × {T_pendulum:.4f} / {De/1000:.3f} = {F_de:.3f} N")

# Force at shaft D (mechanical advantage De/Dd)
F_cd = F_de * (De/Dd)
print(f"   F_cd = {F_de:.3f} × ({De}/{Dd}) = {F_cd:.3f} N")

# Force at shaft C (mechanical advantage Dd/Dc)  
F_bc = F_cd * (Dd/Dc)
print(f"   F_bc = {F_cd:.3f} × ({Dd}/{Dc}) = {F_bc:.3f} N")

# Force at shaft B (mechanical advantage Dc/Db)
F_ab = F_bc * (Dc/Db)
print(f"   F_ab = {F_bc:.3f} × ({Dc}/{Db}) = {F_ab:.3f} N")

print(f"\n6. Expected results from assignment documentation:")
print(f"   F_ab = 392.400 N (calculated: {F_ab:.3f} N)")
print(f"   F_bc = 294.300 N (calculated: {F_bc:.3f} N)") 
print(f"   F_cd = 235.440 N (calculated: {F_cd:.3f} N)")
print(f"   F_de = 181.108 N (calculated: {F_de:.3f} N)")
print(f"   T_motor = 0.3924 N⋅m (calculated: {T_motor:.4f} N⋅m)")

print("="*60)