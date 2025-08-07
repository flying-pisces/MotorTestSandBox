#!/usr/bin/env python3
"""
Parasolid File Conversion Helper
Provides multiple methods to convert .x_t files to usable formats
"""

import os
import subprocess
import urllib.request
import json
from pathlib import Path

def attempt_freecad_conversion(input_file, output_file):
    """Attempt to convert using FreeCAD if available"""
    
    print(f"🔄 Attempting FreeCAD conversion...")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    
    # Try FreeCAD Python API
    try:
        import FreeCAD
        import Import
        
        # Create new document
        doc = FreeCAD.newDocument("ParasolidImport")
        
        # Attempt import
        try:
            Import.insert(input_file, doc.Name)
            doc.recompute()
            
            # Export as STEP
            import Part
            __objs__ = [obj for obj in doc.Objects if hasattr(obj, 'Shape')]
            Part.export(__objs__, output_file)
            
            print(f"✅ Conversion successful: {output_file}")
            return True
            
        except Exception as import_error:
            print(f"❌ FreeCAD import failed: {import_error}")
            return False
            
    except ImportError:
        print("❌ FreeCAD not available in Python environment")
        return False

def create_conversion_instructions():
    """Create detailed conversion instructions"""
    
    instructions = """
# PARASOLID .X_T FILE CONVERSION INSTRUCTIONS

## What Are These Files?
- **assignment1.x_t** and **assignment2.x_t** are Parasolid 3D CAD files
- Created in **SolidWorks 2019** on **August 7, 2025**
- File sizes: ~2.4MB (Assignment1), ~2.1MB (Assignment2)
- Content: Complex 3D geometry with precision surfaces

## CONVERSION METHOD 1: Online Converters (Recommended)

### Option A: eMachineShop (Free, No Signup)
1. Go to: https://convert.emachineshop.com/
2. Upload your .x_t file
3. Select output format: **STEP (.step)** 
4. Download converted file
5. Import STEP file into FreeCAD

### Option B: ConvertCADFiles.com (Free Trial)
1. Go to: https://convertcadfiles.com/
2. Upload .x_t file (max 50KB for free)
3. Convert to STEP format
4. For larger files, pay €1 per conversion

### Option C: CAD Exchanger (Professional)
1. Go to: https://cadexchanger.com/
2. Upload .x_t file
3. Convert to STEP, STL, or other formats
4. Download result

## CONVERSION METHOD 2: Professional Software

### SolidWorks (If Available)
1. Open .x_t file in SolidWorks
2. File → Save As
3. Choose format: **STEP Files (*.step)**
4. Save and use in other CAD software

### Fusion 360 (Free for Personal Use)
1. Download Fusion 360 from Autodesk
2. File → Open → Select .x_t file
3. File → Export → Choose STEP format
4. Use converted file

### FreeCAD (May Work with Newer Versions)
1. Download latest FreeCAD (0.21+)
2. File → Import
3. Select .x_t file
4. If successful, export as STEP

## CONVERSION METHOD 3: Alternative Approaches

### Using 3D Viewer Software
1. Download **3D-Tool Free Viewer**
2. Open .x_t file for viewing
3. Export as STL or other format
4. Import STL into FreeCAD (as mesh)

### Using Online Services
1. **GrabCAD Workbench** - Can sometimes view Parasolid
2. **Onshape** - Import and re-export capability
3. **Tinkercad** - Limited support but worth trying

## WHAT TO EXPECT AFTER CONVERSION

### If Successful:
- 3D geometry will be preserved
- Can integrate with our Method 1 design
- Parametric features may be lost
- Surface quality should remain good

### File Contents Likely Include:
- **Assignment 1:** Torque test fixture/jig
- **Assignment 2:** Pendulum/rope system components
- Complex curved surfaces and precision features
- Assembly components with proper tolerances

## INTEGRATION WITH OUR METHOD 1 DESIGN

Once converted to STEP format:
1. Import into FreeCAD alongside our Method 1 design
2. Compare dimensions and interfaces
3. Adapt our professional design if needed
4. Create hybrid design combining best features

## TROUBLESHOOTING

### If Conversion Fails:
1. Try different online converters
2. Contact original file creator for STEP export
3. Use our professional Method 1 design as baseline
4. Manually recreate critical dimensions

### File Size Issues:
- Original files are large (2+ MB each)
- May need professional converter for full fidelity
- Consider mesh conversion (STL) if solid model fails

## COST ESTIMATE

- **Free options:** eMachineShop, 3D-Tool viewer
- **Low cost:** €1-5 per file via online converters  
- **Professional:** $50-200 for CAD conversion software
- **Alternative:** Use our Method 1 professional design

## NEXT STEPS

1. **Try eMachineShop converter first** (free, reliable)
2. **Compare with our Method 1 design** for integration
3. **Document any design differences** found
4. **Update our CAD models** if needed based on original designs
"""
    
    return instructions

def generate_conversion_report():
    """Generate comprehensive conversion report"""
    
    assignment_files = [
        ("/Users/cyin/project/robot/MotorTestSandBox/Assignment1/assignment1.x_t", "Assignment 1 - Torque Test Setup"),
        ("/Users/cyin/project/robot/MotorTestSandBox/Assignment2/assignment2.x_t", "Assignment 2 - Pendulum System")
    ]
    
    print("📋 PARASOLID CONVERSION REPORT")
    print("=" * 70)
    
    for filepath, description in assignment_files:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"\n📁 {description}")
            print(f"   File: {os.path.basename(filepath)}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Status: Ready for conversion")
            
            # Attempt FreeCAD conversion
            output_step = filepath.replace('.x_t', '_converted.step')
            success = attempt_freecad_conversion(filepath, output_step)
            
            if not success:
                print(f"   Recommendation: Use online converter")
        else:
            print(f"❌ File not found: {filepath}")
    
    print(f"\n" + "=" * 70)
    print("RECOMMENDED CONVERSION WORKFLOW:")
    print("1. Try eMachineShop online converter")
    print("2. Compare converted models with our Method 1 design") 
    print("3. Integrate best features into professional solution")
    print("=" * 70)

def main():
    """Main conversion helper"""
    
    print("PARASOLID .X_T FILE CONVERSION HELPER")
    print("=" * 70)
    
    # Generate conversion report
    generate_conversion_report()
    
    # Create detailed instructions
    instructions = create_conversion_instructions()
    
    # Save instructions to file
    instructions_file = "/Users/cyin/project/robot/MotorTestSandBox/Assignment1/Design/Parasolid_Conversion_Instructions.md"
    with open(instructions_file, 'w') as f:
        f.write(instructions)
    
    print(f"\n📝 Detailed conversion instructions saved to:")
    print(f"   {instructions_file}")
    
    print(f"\n💡 IMMEDIATE ACTION ITEMS:")
    print("1. Visit: https://convert.emachineshop.com/")
    print("2. Upload assignment1.x_t and assignment2.x_t")
    print("3. Convert to STEP format")
    print("4. Download and import into FreeCAD")
    print("5. Compare with our professional Method 1 design")

if __name__ == "__main__":
    main()