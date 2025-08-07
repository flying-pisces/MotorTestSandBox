#!/usr/bin/env python3
"""
Parasolid .x_t File Analyzer
Extracts basic information and geometry data from Parasolid transmit files
"""

import re
import sys
from datetime import datetime

def analyze_parasolid_file(filepath):
    """Analyze a Parasolid .x_t file and extract metadata and basic geometry info"""
    
    print(f"📄 ANALYZING PARASOLID FILE: {filepath}")
    print("=" * 70)
    
    try:
        with open(filepath, 'r', encoding='iso-8859-1') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None
    
    analysis = {
        'metadata': {},
        'geometry': {},
        'statistics': {}
    }
    
    # Extract header metadata
    header_patterns = {
        'creator_app': r'APPL=([^;]+)',
        'parasolid_version': r'FRU=([^;]+)',
        'creation_date': r'DATE=([^;]+)',
        'original_filename': r'FILE=([^;]+)',
        'machine_info': r'MC_MODEL=([^;]+)',
        'os_info': r'OS=([^;]+)',
        'format_type': r'FORMAT=([^;]+)',
        'schema': r'SCH=([^;]+)'
    }
    
    print("📋 METADATA INFORMATION:")
    print("-" * 40)
    
    for key, pattern in header_patterns.items():
        match = re.search(pattern, content)
        if match:
            value = match.group(1).strip()
            analysis['metadata'][key] = value
            print(f"  {key.replace('_', ' ').title():.<20} {value}")
    
    # Count geometry entities
    geometry_patterns = {
        'vertices': r'vertex',
        'edges': r'edge',
        'faces': r'face', 
        'bodies': r'body',
        'curves': r'curve',
        'surfaces': r'surface',
        'transforms': r'transform'
    }
    
    print(f"\n🔢 GEOMETRY STATISTICS:")
    print("-" * 40)
    
    for entity, pattern in geometry_patterns.items():
        count = len(re.findall(pattern, content, re.IGNORECASE))
        if count > 0:
            analysis['geometry'][entity] = count
            print(f"  {entity.capitalize():.<15} {count}")
    
    # Extract coordinate data (sample)
    coord_pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    coordinates = re.findall(coord_pattern, content)
    numeric_coords = []
    
    try:
        for coord in coordinates[:100]:  # Sample first 100 coordinates
            try:
                val = float(coord)
                if abs(val) > 1e-10:  # Filter out near-zero values
                    numeric_coords.append(val)
            except:
                continue
                
        if numeric_coords:
            analysis['statistics']['coord_range_min'] = min(numeric_coords)
            analysis['statistics']['coord_range_max'] = max(numeric_coords)
            analysis['statistics']['sample_coords'] = len(numeric_coords)
    except:
        pass
    
    # File statistics
    analysis['statistics']['file_size_kb'] = len(content) / 1024
    analysis['statistics']['total_lines'] = len(content.split('\n'))
    
    print(f"\n📊 FILE STATISTICS:")
    print("-" * 40)
    print(f"  File Size:........... {analysis['statistics']['file_size_kb']:.1f} KB")
    print(f"  Total Lines:......... {analysis['statistics']['total_lines']}")
    
    if 'sample_coords' in analysis['statistics']:
        print(f"  Coordinate Samples:.. {analysis['statistics']['sample_coords']}")
        print(f"  Coord Range Min:..... {analysis['statistics']['coord_range_min']:.6f}")
        print(f"  Coord Range Max:..... {analysis['statistics']['coord_range_max']:.6f}")
    
    # Detect potential geometry type
    content_lower = content.lower()
    geometry_hints = []
    
    if 'cylinder' in content_lower:
        geometry_hints.append('Cylindrical features')
    if 'sphere' in content_lower:
        geometry_hints.append('Spherical features')
    if 'plane' in content_lower:
        geometry_hints.append('Planar surfaces')
    if 'cone' in content_lower:
        geometry_hints.append('Conical features')
    if 'torus' in content_lower:
        geometry_hints.append('Toroidal features')
    
    if geometry_hints:
        print(f"\n🔍 DETECTED GEOMETRY TYPES:")
        print("-" * 40)
        for hint in geometry_hints:
            print(f"  • {hint}")
    
    return analysis

def suggest_conversion_methods():
    """Suggest methods to convert Parasolid files"""
    
    print(f"\n🔄 CONVERSION OPTIONS:")
    print("=" * 70)
    
    methods = [
        {
            'method': 'FreeCAD with Parasolid Plugin',
            'description': 'Install FreeCAD with Parasolid import capability',
            'steps': [
                '1. Download FreeCAD from freecadweb.org',
                '2. Install Parasolid import plugin if available',
                '3. File → Import → Select .x_t file',
                '4. Export as STEP (.step) or STL format'
            ],
            'success_rate': 'High'
        },
        {
            'method': 'Online CAD Converters',
            'description': 'Use web-based conversion services',
            'steps': [
                '1. Upload .x_t file to online converter',
                '2. Convert to STEP, STL, or OBJ format',
                '3. Download converted file',
                '4. Import into FreeCAD or other CAD software'
            ],
            'success_rate': 'Medium',
            'services': ['CAD Exchanger', 'AnyCAD', '3D Tool']
        },
        {
            'method': 'SolidWorks/Professional CAD',
            'description': 'Use original software or compatible CAD',
            'steps': [
                '1. Open in SolidWorks, Inventor, or Fusion 360',
                '2. Export as STEP (.step) neutral format',
                '3. Import STEP file into FreeCAD',
                '4. Continue with design modifications'
            ],
            'success_rate': 'Very High'
        },
        {
            'method': 'Parasolid SDK/Libraries',
            'description': 'Use Parasolid reading libraries',
            'steps': [
                '1. Use Open3D or similar libraries',
                '2. Convert to mesh format (STL, OBJ)',
                '3. Import mesh into CAD software',
                '4. May lose parametric features'
            ],
            'success_rate': 'Medium'
        }
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n{i}. {method['method']}")
        print(f"   {method['description']}")
        print(f"   Success Rate: {method['success_rate']}")
        print("   Steps:")
        for step in method['steps']:
            print(f"     {step}")
        if 'services' in method:
            print(f"   Services: {', '.join(method['services'])}")

def main():
    """Main analysis function"""
    
    # Analyze both assignment files
    assignment_files = [
        "/Users/cyin/project/robot/MotorTestSandBox/Assignment1/assignment1.x_t",
        "/Users/cyin/project/robot/MotorTestSandBox/Assignment2/assignment2.x_t"
    ]
    
    for filepath in assignment_files:
        analyze_parasolid_file(filepath)
        print("\n" + "=" * 70 + "\n")
    
    suggest_conversion_methods()
    
    print(f"\n💡 RECOMMENDATIONS:")
    print("=" * 70)
    print("1. Try FreeCAD import first - may work with newer versions")
    print("2. Use online converter to convert to STEP format")
    print("3. Contact original designer for STEP exports")
    print("4. Use our professional Method 1 CAD design as reference")

if __name__ == "__main__":
    main()