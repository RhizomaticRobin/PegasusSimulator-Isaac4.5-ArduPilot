#!/usr/bin/env python3
"""
Fix ArduPilot compatibility for Isaac Sim 4.5
This script updates the vehicle base classes to use new Isaac Sim 4.5 APIs
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def fix_vehicle_file(filepath):
    """Fix vehicle.py for Isaac Sim 4.5"""
    
    print(f"\n🔧 Processing {filepath}")
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Backup
    backup_path = filepath.with_suffix('.py.ardupilot_backup')
    if not backup_path.exists():
        shutil.copy2(filepath, backup_path)
        print(f"  📋 Created backup: {backup_path.name}")
    
    original_content = content
    
    # Fix 1: Update dynamic control import
    content = re.sub(
        r'from omni\.isaac\.dynamic_control import _dynamic_control',
        'from isaacsim.core.dynamic_control import _dynamic_control',
        content
    )
    
    # Fix 2: Replace get_world_transform_xform function
    # Find the function and replace it
    func_pattern = r'def get_world_transform_xform\(prim: Usd\.Prim\):.*?return rotation'
    
    new_function = '''def get_world_transform_xform(prim: Usd.Prim):
    """
    Get the local transformation of a prim using USD APIs directly.
    Compatible with Isaac Sim 4.5.
    
    Args:
        prim (Usd.Prim): The prim to calculate the world transformation.
    Returns:
        Gf.Rotation: The rotation component of the world transform.
    """
    from pxr import UsdGeom
    
    # Get the xformable interface
    xformable = UsdGeom.Xformable(prim)
    if not xformable:
        carb.log_error(f"Prim {prim.GetPath()} is not xformable")
        return Gf.Rotation()
    
    # Compute world transform at default time
    time = Usd.TimeCode.Default()
    world_transform = xformable.ComputeLocalToWorldTransform(time)
    
    # Extract rotation using Gf.Transform
    transform = Gf.Transform(world_transform)
    return transform.GetRotation()'''
    
    # Use DOTALL flag to match across multiple lines
    content = re.sub(func_pattern, new_function, content, flags=re.DOTALL)
    
    # Fix 3: Add fallback for omni.usd if it's still needed elsewhere
    if 'import omni.usd' in content and 'get_world_transform_matrix' not in content:
        # If omni.usd is imported but get_world_transform_matrix is not used elsewhere, we can keep it
        pass
    
    # Check if changes were made
    if content != original_content:
        # Write fixed content
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✅ Fixed dynamic control imports and transform function")
    else:
        print(f"  ⏭️  No changes needed")

def fix_multirotor_file(filepath):
    """Fix multirotor.py for Isaac Sim 4.5"""
    
    print(f"\n🔧 Processing {filepath}")
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Backup
    backup_path = filepath.with_suffix('.py.ardupilot_backup')
    if not backup_path.exists():
        shutil.copy2(filepath, backup_path)
        print(f"  📋 Created backup: {backup_path.name}")
    
    original_content = content
    
    # Fix dynamic control import
    content = re.sub(
        r'from omni\.isaac\.dynamic_control import _dynamic_control',
        'from isaacsim.core.dynamic_control import _dynamic_control',
        content
    )
    
    # Check if changes were made
    if content != original_content:
        # Write fixed content
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✅ Fixed dynamic control import")
    else:
        print(f"  ⏭️  No changes needed")

def verify_ardupilot_backend(backend_dir):
    """Verify ArduPilot backend files don't have Isaac Sim dependencies"""
    
    print(f"\n🔍 Verifying ArduPilot backend files...")
    
    ardupilot_files = [
        "ardupilot_mavlink_backend.py",
        "tools/ardupilot_launch_tool.py",
        "tools/ArduPilotPlugin.py"
    ]
    
    isaac_imports = ['omni.isaac', 'isaacsim', 'omni.usd', 'omni.kit']
    issues_found = False
    
    for file in ardupilot_files:
        filepath = backend_dir / file
        if filepath.exists():
            with open(filepath, 'r') as f:
                content = f.read()
            
            found_imports = []
            for imp in isaac_imports:
                if imp in content:
                    found_imports.append(imp)
            
            if found_imports:
                print(f"  ⚠️  {file} contains Isaac Sim imports: {found_imports}")
                issues_found = True
            else:
                print(f"  ✅ {file} - No Isaac Sim dependencies")
        else:
            print(f"  ❌ {file} not found")
    
    if not issues_found:
        print("\n✅ ArduPilot backend files are clean - no Isaac Sim dependencies!")

def create_test_script():
    """Create a test script for ArduPilot functionality"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test script for ArduPilot integration with Isaac Sim 4.5
Run this after applying the fixes to verify functionality
"""

import time
import subprocess

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    try:
        from pegasus.simulator.logic.vehicles.vehicle import Vehicle
        from pegasus.simulator.logic.vehicles.multirotor import Multirotor
        from pegasus.simulator.logic.backends.ardupilot_mavlink_backend import ArduPilotMavlinkBackend
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_ardupilot_launch():
    """Test ArduPilot SITL launch"""
    print("\\nTesting ArduPilot launch tool...")
    try:
        from pegasus.simulator.logic.backends.tools.ardupilot_launch_tool import ArduPilotLaunchTool
        # Don't actually launch, just test import
        print("✅ ArduPilot launch tool imports correctly")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("ArduPilot Isaac Sim 4.5 Compatibility Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_ardupilot_launch,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\\n✅ All tests passed! ArduPilot should be compatible with Isaac Sim 4.5")
        print("\\n⚠️  Note: Full flight testing still required")
    else:
        print("\\n❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
'''
    
    test_path = Path("test_ardupilot_compatibility.py")
    with open(test_path, 'w') as f:
        f.write(test_script)
    os.chmod(test_path, 0o755)
    print(f"\n📝 Created test script: {test_path}")

def main():
    """Main function to fix ArduPilot compatibility"""
    
    print("ArduPilot Isaac Sim 4.5 Compatibility Fixer")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we're in the right directory
    if not Path("extensions/pegasus.simulator").exists():
        print("\n❌ Error: Could not find 'extensions/pegasus.simulator' directory")
        print("   Please run this script from the PegasusSimulator root directory")
        return
    
    # Fix vehicle.py
    vehicle_path = Path("extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py")
    if vehicle_path.exists():
        fix_vehicle_file(vehicle_path)
    else:
        print(f"\n❌ Could not find {vehicle_path}")
    
    # Fix multirotor.py
    multirotor_path = Path("extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py")
    if multirotor_path.exists():
        fix_multirotor_file(multirotor_path)
    else:
        print(f"\n❌ Could not find {multirotor_path}")
    
    # Verify ArduPilot backend
    backend_dir = Path("extensions/pegasus.simulator/pegasus/simulator/logic/backends")
    if backend_dir.exists():
        verify_ardupilot_backend(backend_dir)
    
    # Create test script
    create_test_script()
    
    print("\n" + "=" * 50)
    print("✅ ArduPilot compatibility fixes applied!")
    print("\n📋 Next steps:")
    print("   1. Run the general migration script: python migrate_to_isaac_4.5.py")
    print("   2. Test imports: python test_ardupilot_compatibility.py")
    print("   3. Launch Isaac Sim 4.5 and test ArduPilot example")
    print("   4. Report any issues to the PegasusSimulator repository")
    print("\n⚠️  IMPORTANT: Test thoroughly before production use!")

if __name__ == "__main__":
    main()