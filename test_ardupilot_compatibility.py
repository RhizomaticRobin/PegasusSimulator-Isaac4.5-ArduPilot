#!/usr/bin/env python3
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
    print("\nTesting ArduPilot launch tool...")
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
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✅ All tests passed! ArduPilot should be compatible with Isaac Sim 4.5")
        print("\n⚠️  Note: Full flight testing still required")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
