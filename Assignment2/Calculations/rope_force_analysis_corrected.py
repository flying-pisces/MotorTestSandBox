#!/usr/bin/env python3
"""
Assignment 2: Rope Transmission System Analysis (CORRECTED)
Calculates rope forces and motor torque for pendulum testbed

System Parameters:
- Pendulum: M = 2kg, L = 0.3m (massless bar)
- Shaft diameters: Da=20mm, Db=30mm, Dc=40mm, Dd=50mm, De=65mm  
- Gearbox ratio: 10:1
- Analysis condition: Pendulum horizontal (0°) - maximum torque

Key Fix: Corrected torque direction - motor provides LESS torque than load due to mechanical advantage
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json
import os

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
        # Key insight: Each rope stage provides mechanical advantage
        # Smaller pulley driving larger pulley: Force increases, Torque decreases
        
        # From E to D: Force increases by diameter ratio (De/Dd)
        F_cd = F_de * (self.De / self.Dd)
        T_d = F_cd * (self.Dd / 2)  # Torque at shaft D
        
        # From D to C: Force increases by diameter ratio (Dd/Dc)  
        F_bc = F_cd * (self.Dd / self.Dc)
        T_c = F_bc * (self.Dc / 2)  # Torque at shaft C
        
        # From C to B: Force increases by diameter ratio (Dc/Db)
        F_ab = F_bc * (self.Dc / self.Db)
        T_b = F_ab * (self.Db / 2)  # Torque at shaft B
        
        # From B to A: The torque after gearbox is the torque required at shaft A
        # T_a = F_ab * (Da/2), but this is the torque after gearbox reduction
        T_after_gearbox = F_ab * (self.Da / 2)
        
        # Motor torque before gearbox (motor output)
        # Gearbox provides 10:1 reduction, so motor torque is lower
        T_motor = T_after_gearbox / self.gear_ratio
        
        # Store results
        self.results.update({
            'F_de': F_de,
            'F_cd': F_cd, 
            'F_bc': F_bc,
            'F_ab': F_ab,
            'T_motor': T_motor,
            'T_after_gearbox': T_after_gearbox,
            'torques': {
                'T_e': T_e,
                'T_d': T_d, 
                'T_c': T_c,
                'T_b': T_b,
                'T_after_gearbox': T_after_gearbox
            }
        })
        
        return {
            'F_ab': F_ab,
            'F_bc': F_bc, 
            'F_cd': F_cd,
            'F_de': F_de
        }
    
    def verify_calculations(self):
        """Verify calculations using total mechanical advantage approach"""
        # Total mechanical advantage = rope reduction × gearbox reduction
        rope_reduction = (self.De/self.Dd) * (self.Dd/self.Dc) * (self.Dc/self.Db) * (self.Db/self.Da)
        total_reduction = rope_reduction * self.gear_ratio
        
        T_pendulum = self.results['torque_pendulum']
        T_motor_alt = T_pendulum / total_reduction
        
        error = abs(self.results['T_motor'] - T_motor_alt) / T_motor_alt * 100
        
        self.results['verification'] = {
            'rope_reduction_ratio': rope_reduction,
            'total_reduction_ratio': total_reduction,
            'T_motor_alternative': T_motor_alt,
            'error_percentage': error
        }
        
        return error < 1.0  # Error should be < 1%
    
    def generate_force_diagram(self):
        """Create visual representation of force transmission"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Rope forces
        ropes = ['F_ab', 'F_bc', 'F_cd', 'F_de']
        forces = [self.results[rope] for rope in ropes]
        
        ax1.bar(ropes, forces, color=['red', 'blue', 'green', 'orange'])
        ax1.set_ylabel('Force (N)')
        ax1.set_title('Rope Forces in Transmission System')
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(forces):
            ax1.text(i, v + max(forces)*0.01, f'{v:.1f} N', ha='center', va='bottom')
        
        # Plot 2: Torque progression through system
        stages = ['Motor', 'After Gearbox', 'Shaft B', 'Shaft C', 'Shaft D', 'Shaft E']
        torques = [
            self.results['T_motor'],
            self.results['T_after_gearbox'], 
            self.results['torques']['T_b'],
            self.results['torques']['T_c'],
            self.results['torques']['T_d'],
            self.results['torques']['T_e']
        ]
        
        ax2.plot(stages, torques, 'o-', linewidth=2, markersize=8)
        ax2.set_ylabel('Torque (N⋅m)')
        ax2.set_title('Torque Progression Through System')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for i, v in enumerate(torques):
            ax2.text(i, v + max(torques)*0.02, f'{v:.3f} N⋅m', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Create output directory if it doesn't exist
        output_dir = '../Output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.savefig(f'{output_dir}/force_analysis_corrected.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def export_results(self, filename=None):
        """Export results in clean format"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'../Output/results_corrected_{timestamp}'
        
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
        
        # Create output directory if it doesn't exist
        output_dir = '../Output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save as JSON
        with open(f'{filename}.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save as CSV for easy analysis
        df_forces = pd.DataFrame({
            'Rope_Segment': ['AB', 'BC', 'CD', 'DE'],
            'Force_N': [self.results['F_ab'], self.results['F_bc'], 
                       self.results['F_cd'], self.results['F_de']],
            'Shaft_From': ['A', 'B', 'C', 'D'],
            'Shaft_To': ['B', 'C', 'D', 'E'],
            'Diameter_From_mm': [self.Da*1000, self.Db*1000, self.Dc*1000, self.Dd*1000],
            'Diameter_To_mm': [self.Db*1000, self.Dc*1000, self.Dd*1000, self.De*1000]
        })
        df_forces.to_csv(f'{filename}_forces.csv', index=False)
        
        return report
    
    def print_summary(self):
        """Print formatted summary of results"""
        print("="*60)
        print("ASSIGNMENT 2: ROPE TRANSMISSION ANALYSIS (CORRECTED)")
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
        print(f"  Motor Torque (Tm): {self.results['T_motor']:.4f} N⋅m")
        print(f"  After Gearbox: {self.results['T_after_gearbox']:.4f} N⋅m")
        print(f"  Pendulum Load: {self.results['torque_pendulum']:.4f} N⋅m")
        print()
        
        print("VERIFICATION:")
        print(f"  Rope Reduction Ratio: {self.results['verification']['rope_reduction_ratio']:.2f}")
        print(f"  Total Reduction Ratio: {self.results['verification']['total_reduction_ratio']:.2f}")
        print(f"  Calculation Error: {self.results['verification']['error_percentage']:.6f}%")
        
        # Sanity check
        if self.results['T_motor'] < self.results['torque_pendulum']:
            print("  ✅ SANITY CHECK PASSED: Motor torque < Load torque (mechanical advantage)")
        else:
            print("  ❌ SANITY CHECK FAILED: Motor torque >= Load torque")
        
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
    
    # Generate visualizations
    analysis.generate_force_diagram()
    
    # Export results
    report = analysis.export_results()
    
    print(f"\nResults exported to ../Output/")
    print(f"Calculation verification: {'PASSED' if is_valid else 'FAILED'}")