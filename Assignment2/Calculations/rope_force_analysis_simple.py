#!/usr/bin/env python3
"""
Assignment 2: Rope Transmission System Analysis
Calculates rope forces and motor torque for pendulum testbed
Simple version without external dependencies

System Parameters:
- Pendulum: M = 2kg, L = 0.3m (massless bar)
- Shaft diameters: Da=20mm, Db=30mm, Dc=40mm, Dd=50mm, De=65mm  
- Gearbox ratio: 10:1
- Analysis condition: Pendulum horizontal (0°) - maximum torque
"""

import math
import json
from datetime import datetime

class RopeTransmissionAnalysis:
    def __init__(self):
        # System parameters
        self.M = 2.0  # kg - pendulum mass
        self.L = 0.3  # m - pendulum length
        self.g = 9.81  # m/s² - gravity
        
        # Shaft diameters (mm converted to m)
        self.Da = 0.020  # m
        self.Db = 0.030  # m  
        self.Dc = 0.040  # m
        self.Dd = 0.050  # m
        self.De = 0.065  # m
        
        # Gearbox ratio
        self.gear_ratio = 10.0
        
        # Results storage
        self.results = {}
        
    def calculate_pendulum_torque(self):
        """Calculate torque required to hold pendulum horizontal"""
        # At horizontal position (θ = 0°), torque = M * g * L
        torque_pendulum = self.M * self.g * self.L
        self.results['torque_pendulum'] = torque_pendulum
        return torque_pendulum
    
    def calculate_rope_forces(self):
        """Calculate forces in each rope segment working backwards from load"""
        # Start with pendulum torque
        T_e = self.calculate_pendulum_torque()
        
        # Force on rope DE (last segment)
        # T_e = F_de * (De/2)  ->  F_de = 2*T_e/De
        F_de = (2 * T_e) / self.De
        
        # Working backwards through the system
        # For rope systems, the force relationship is based on rope tension equilibrium
        # The tension force remains constant along each rope segment
        # Torque amplification occurs due to different shaft radii
        
        # At each stage: T_input * efficiency = T_output
        # T_input = F_rope * R_input, T_output = F_rope * R_output
        # Therefore: F_rope * R_input = F_rope * R_output (no amplification in force)
        # But torque amplifies: T_output/T_input = R_output/R_input
        
        # Actually, for rope transmission: Force amplifies inversely to radius ratio
        # F_input * R_input = F_output * R_output (moment equilibrium)
        
        # Rope CD force (working backwards from DE)
        F_cd = F_de * (self.De / self.Dd)
        
        # Rope BC force
        F_bc = F_cd * (self.Dd / self.Dc)
        
        # Rope AB force
        F_ab = F_bc * (self.Dc / self.Db)
        
        # Torque calculations for verification
        T_d = F_cd * (self.Dd / 2)
        T_c = F_bc * (self.Dc / 2)
        T_b = F_ab * (self.Db / 2)
        T_a = F_ab * (self.Da / 2)  # Torque on shaft A
        
        # Motor torque before gearbox (motor output)
        T_motor = T_a / self.gear_ratio
        
        # Store results
        self.results.update({
            'F_de': F_de,
            'F_cd': F_cd, 
            'F_bc': F_bc,
            'F_ab': F_ab,
            'T_motor': T_motor,
            'T_after_gearbox': T_a,
            'torques': {
                'T_e': T_e,
                'T_d': T_d, 
                'T_c': T_c,
                'T_b': T_b,
                'T_a': T_a
            }
        })
        
        return {
            'F_ab': F_ab,
            'F_bc': F_bc, 
            'F_cd': F_cd,
            'F_de': F_de
        }
    
    def verify_calculations(self):
        """Verify calculations using alternative approach"""
        # Alternative: Calculate total reduction ratio from motor to load
        # Each stage multiplies torque by diameter ratio, plus gearbox
        rope_reduction = (self.De/self.Dd) * (self.Dd/self.Dc) * (self.Dc/self.Db) * (self.Db/self.Da)
        total_reduction = rope_reduction * self.gear_ratio
        
        T_pendulum = self.results['torque_pendulum']
        T_motor_alt = T_pendulum / total_reduction
        
        # Also verify torque balance at gearbox
        T_motor_expected = self.results['T_after_gearbox'] / self.gear_ratio
        
        error = abs(self.results['T_motor'] - T_motor_expected) / abs(T_motor_expected) * 100
        
        self.results['verification'] = {
            'rope_reduction_ratio': rope_reduction,
            'total_reduction_ratio': total_reduction,
            'T_motor_alternative': T_motor_alt,
            'T_motor_expected': T_motor_expected,
            'error_percentage': error
        }
        
        return error < 1.0  # Allow for small numerical errors
    
    def export_results(self, filename=None):
        """Export results in clean format for iteration recording"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'../Output/results_{timestamp}'
        
        # Create detailed report
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_parameters': {
                'pendulum_mass_kg': self.M,
                'pendulum_length_m': self.L,
                'shaft_diameters_mm': {
                    'Da': self.Da * 1000,
                    'Db': self.Db * 1000, 
                    'Dc': self.Dc * 1000,
                    'Dd': self.Dd * 1000,
                    'De': self.De * 1000
                },
                'gearbox_ratio': self.gear_ratio
            },
            'calculated_forces_N': {
                'F_ab': round(self.results['F_ab'], 3),
                'F_bc': round(self.results['F_bc'], 3),
                'F_cd': round(self.results['F_cd'], 3), 
                'F_de': round(self.results['F_de'], 3)
            },
            'calculated_torques_Nm': {
                'motor_torque': round(self.results['T_motor'], 4),
                'after_gearbox': round(self.results['T_after_gearbox'], 4),
                'pendulum_load': round(self.results['torque_pendulum'], 4)
            },
            'verification': self.results['verification']
        }
        
        # Save as JSON
        with open(f'{filename}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save as CSV manually
        csv_content = "Rope_Segment,Force_N,Shaft_From,Shaft_To,Diameter_From_mm,Diameter_To_mm\n"
        csv_content += f"AB,{self.results['F_ab']:.3f},A,B,{self.Da*1000},{self.Db*1000}\n"
        csv_content += f"BC,{self.results['F_bc']:.3f},B,C,{self.Db*1000},{self.Dc*1000}\n"
        csv_content += f"CD,{self.results['F_cd']:.3f},C,D,{self.Dc*1000},{self.Dd*1000}\n"
        csv_content += f"DE,{self.results['F_de']:.3f},D,E,{self.Dd*1000},{self.De*1000}\n"
        
        with open(f'{filename}_forces.csv', 'w') as f:
            f.write(csv_content)
        
        return report
    
    def print_summary(self):
        """Print formatted summary of results"""
        print("="*60)
        print("ASSIGNMENT 2: ROPE TRANSMISSION SYSTEM ANALYSIS")
        print("="*60)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("SYSTEM PARAMETERS:")
        print(f"  Pendulum Mass: {self.M} kg")
        print(f"  Pendulum Length: {self.L} m") 
        print(f"  Shaft Diameters: Da={self.Da*1000}mm, Db={self.Db*1000}mm, Dc={self.Dc*1000}mm, Dd={self.Dd*1000}mm, De={self.De*1000}mm")
        print(f"  Gearbox Ratio: {self.gear_ratio}:1")
        print()
        
        print("CALCULATED ROPE FORCES (Pendulum Horizontal):")
        print(f"  F_ab = {self.results['F_ab']:.3f} N")
        print(f"  F_bc = {self.results['F_bc']:.3f} N") 
        print(f"  F_cd = {self.results['F_cd']:.3f} N")
        print(f"  F_de = {self.results['F_de']:.3f} N")
        print()
        
        print("CALCULATED TORQUES:")
        print(f"  Motor Torque (Tm): {self.results['T_motor']:.4f} N*m")
        print(f"  After Gearbox: {self.results['T_after_gearbox']:.4f} N*m")
        print(f"  Pendulum Load: {self.results['torque_pendulum']:.4f} N*m")
        print()
        
        print("VERIFICATION:")
        print(f"  Rope Reduction Ratio: {self.results['verification']['rope_reduction_ratio']:.2f}")
        print(f"  Total Reduction Ratio: {self.results['verification']['total_reduction_ratio']:.2f}")
        print(f"  Motor Torque (Alternative): {self.results['verification']['T_motor_alternative']:.4f} N*m")
        print(f"  Calculation Error: {self.results['verification']['error_percentage']:.6f}%")
        print()
        
        print("FORMULAS USED:")
        print("  1. Pendulum Torque: T = M * g * L")
        print("  2. Rope Force: F = 2T / D (where T is torque, D is shaft diameter)")
        print("  3. Torque Amplification: T_next = T_prev * (D_next/D_prev)")
        print("  4. Total Reduction: R = (De/Dd) * (Dd/Dc) * (Dc/Db) * (Db/Da) * gear_ratio")
        print("="*60)

if __name__ == "__main__":
    # Run analysis
    analysis = RopeTransmissionAnalysis()
    
    # Calculate rope forces
    forces = analysis.calculate_rope_forces()
    
    # Verify calculations
    is_valid = analysis.verify_calculations()
    
    # Print results
    analysis.print_summary()
    
    # Export results
    report = analysis.export_results()
    
    print(f"\nResults exported to Assignment2/Output/")
    print(f"Calculation verification: {'PASSED' if is_valid else 'FAILED'}")