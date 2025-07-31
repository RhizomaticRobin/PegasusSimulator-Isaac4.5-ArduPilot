# ArduPilot Compatibility Fix Plan for Isaac Sim 4.5

## Executive Summary

This plan details the specific changes needed to make ArduPilot backend compatible with Isaac Sim 4.5. The good news is that the ArduPilot backend itself doesn't directly use Isaac Sim APIs - the issues are concentrated in the vehicle base class and its interaction with Isaac Sim's physics and rendering APIs.

## 1. Architecture Overview

### Current Data Flow:
```
Isaac Sim Physics → Vehicle.update_state() → State Object → Sensors → ArduPilot Backend → MAVLINK/JSON
```

### Key Components:
1. **Vehicle.py** - Interfaces with Isaac Sim APIs (BROKEN)
2. **Sensors** (IMU, GPS, Barometer, Magnetometer) - Work with State objects (OK)
3. **ArduPilot Backend** - MAVLINK/JSON communication (OK)
4. **Coordinate Transformations** - ENU to NED conversions (OK)

## 2. Specific Issues and Fixes

### Issue 1: World Transform API Change
**File:** `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py`
**Line:** 299

**Current Code:**
```python
# Line 16: Import
import omni.usd

# Line 42: Function call
world_transform: Gf.Matrix4d = omni.usd.get_world_transform_matrix(prim)
```

**Fix:**
```python
# Updated import (if API changed)
import omni.usd  # Check if namespace changed

# Alternative approach using pxr USD APIs directly
from pxr import UsdGeom

# In get_world_transform_xform function:
def get_world_transform_xform(prim: Usd.Prim):
    """Get world transform using USD APIs"""
    xformable = UsdGeom.Xformable(prim)
    time = Usd.TimeCode.Default()
    world_transform = xformable.ComputeLocalToWorldTransform(time)
    return Gf.Transform(world_transform).GetRotation()
```

### Issue 2: Dynamic Control API Updates
**File:** `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py`
**Line:** 21, 109, 293, etc.

**Current Code:**
```python
from omni.isaac.dynamic_control import _dynamic_control
```

**Fix:**
```python
from isaacsim.core.dynamic_control import _dynamic_control
```

### Issue 3: Core API Imports
**File:** `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py`
**Lines:** 18-20

**Current Code:**
```python
from isaacsim.core.utils.prims import define_prim, get_prim_at_path
from isaacsim.core.api.robots.robot import Robot
```

**Fix:**
```python
# Already correct - these follow new pattern
from isaacsim.core.utils.prims import define_prim, get_prim_at_path
from isaacsim.core.api.robots.robot import Robot
```

## 3. Detailed Migration Steps

### Step 1: Update Vehicle Base Class

Create a patch file `ardupilot_vehicle_fix.patch`:

```python
--- a/extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py
+++ b/extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py
@@ -19,7 +19,7 @@ import omni.usd
 from isaacsim.core.utils.prims import define_prim, get_prim_at_path
 from omni.usd import get_stage_next_free_path
 from isaacsim.core.api.robots.robot import Robot
-from omni.isaac.dynamic_control import _dynamic_control
+from isaacsim.core.dynamic_control import _dynamic_control
 
 # Extension APIs
 from pegasus.simulator.logic.state import State
@@ -39,9 +39,13 @@ def get_world_transform_xform(prim: Usd.Prim):
         - Rotation quaternion, i.e. 3d vector plus angle.
         - Scale vector.
     """
-    world_transform: Gf.Matrix4d = omni.usd.get_world_transform_matrix(prim)
-    rotation: Gf.Rotation = world_transform.ExtractRotation()
-    return rotation
+    # Use USD APIs directly for better compatibility
+    from pxr import UsdGeom
+    xformable = UsdGeom.Xformable(prim)
+    time = Usd.TimeCode.Default()
+    world_transform = xformable.ComputeLocalToWorldTransform(time)
+    transform = Gf.Transform(world_transform)
+    return transform.GetRotation()
 
 
 class Vehicle(Robot):
```

### Step 2: Update Multirotor Class

**File:** `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py`
**Line:** 10

```python
# OLD
from omni.isaac.dynamic_control import _dynamic_control
# NEW
from isaacsim.core.dynamic_control import _dynamic_control
```

### Step 3: Verify Sensor Interfaces

The sensors (IMU, GPS, Barometer, Magnetometer) don't need changes as they work with State objects and don't directly interface with Isaac Sim APIs.

### Step 4: Test ArduPilot Communication

No changes needed in:
- `ardupilot_mavlink_backend.py`
- `ardupilot_launch_tool.py`
- `ArduPilotPlugin.py`

These files handle MAVLINK/JSON communication and don't use Isaac Sim APIs.

## 4. Testing Plan

### Phase 1: Basic Functionality
1. **Vehicle State Updates**
   - Verify position tracking works
   - Verify orientation (quaternion) updates correctly
   - Check linear/angular velocity calculations

2. **Sensor Data Flow**
   - Confirm IMU data generation
   - Verify GPS coordinate calculations
   - Check barometer altitude readings
   - Test magnetometer orientation

### Phase 2: ArduPilot Integration
1. **SITL Connection**
   - Launch ArduPilot SITL
   - Verify MAVLINK connection establishment
   - Check heartbeat messages

2. **Data Exchange**
   - Verify HIL_SENSOR messages
   - Check HIL_GPS messages
   - Confirm motor commands reception
   - Test arm/disarm functionality

### Phase 3: Flight Testing
1. **Basic Hover Test**
   - Arm vehicle
   - Take off to 5m
   - Hold position for 30s
   - Land

2. **Navigation Test**
   - Simple waypoint mission
   - Return to launch
   - Verify position accuracy

## 5. Implementation Script

Save as `fix_ardupilot_for_isaac_4.5.py`:

```python
#!/usr/bin/env python3
"""
Fix ArduPilot compatibility for Isaac Sim 4.5
"""

import os
import re
import shutil
from pathlib import Path

def fix_vehicle_file(filepath):
    """Fix vehicle.py for Isaac Sim 4.5"""
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Backup
    shutil.copy2(filepath, filepath + '.ardupilot_backup')
    
    # Fix dynamic control import
    content = re.sub(
        r'from omni\.isaac\.dynamic_control import',
        'from isaacsim.core.dynamic_control import',
        content
    )
    
    # Fix get_world_transform_xform function
    old_func = r"""def get_world_transform_xform\(prim: Usd\.Prim\):
    \"\"\"
    Get the local transformation of a prim using omni\.usd\.get_world_transform_matrix\(\)\.
    See https://docs\.omniverse\.nvidia\.com/kit/docs/omni\.usd/latest/omni\.usd/omni\.usd\.get_world_transform_matrix\.html
    Args:
        prim \(Usd\.Prim\): The prim to calculate the world transformation\.
    Returns:
        A tuple of:
        - Translation vector\.
        - Rotation quaternion, i\.e\. 3d vector plus angle\.
        - Scale vector\.
    \"\"\"
    world_transform: Gf\.Matrix4d = omni\.usd\.get_world_transform_matrix\(prim\)
    rotation: Gf\.Rotation = world_transform\.ExtractRotation\(\)
    return rotation"""
    
    new_func = '''def get_world_transform_xform(prim: Usd.Prim):
    """
    Get the local transformation of a prim using USD APIs.
    Args:
        prim (Usd.Prim): The prim to calculate the world transformation.
    Returns:
        A tuple of:
        - Translation vector.
        - Rotation quaternion, i.e. 3d vector plus angle.
        - Scale vector.
    """
    from pxr import UsdGeom
    xformable = UsdGeom.Xformable(prim)
    time = Usd.TimeCode.Default()
    world_transform = xformable.ComputeLocalToWorldTransform(time)
    transform = Gf.Transform(world_transform)
    return transform.GetRotation()'''
    
    content = re.sub(old_func, new_func, content, flags=re.DOTALL)
    
    # Write fixed content
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {filepath}")

def fix_multirotor_file(filepath):
    """Fix multirotor.py for Isaac Sim 4.5"""
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Backup
    shutil.copy2(filepath, filepath + '.ardupilot_backup')
    
    # Fix dynamic control import
    content = re.sub(
        r'from omni\.isaac\.dynamic_control import',
        'from isaacsim.core.dynamic_control import',
        content
    )
    
    # Write fixed content
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {filepath}")

def main():
    """Main function to fix ArduPilot compatibility"""
    
    print("ArduPilot Isaac Sim 4.5 Compatibility Fixer")
    print("=" * 50)
    
    # Fix vehicle.py
    vehicle_path = Path("extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py")
    if vehicle_path.exists():
        fix_vehicle_file(vehicle_path)
    else:
        print(f"❌ Could not find {vehicle_path}")
    
    # Fix multirotor.py
    multirotor_path = Path("extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py")
    if multirotor_path.exists():
        fix_multirotor_file(multirotor_path)
    else:
        print(f"❌ Could not find {multirotor_path}")
    
    print("\n✅ ArduPilot compatibility fixes applied!")
    print("\n⚠️  Please test thoroughly before production use")

if __name__ == "__main__":
    main()
```

## 6. Known Limitations

1. **Physics Engine Changes** - Isaac Sim 4.5 may have physics timing changes that affect SITL synchronization
2. **Dynamic Control API** - Some functions may have changed signatures
3. **Performance** - New APIs may have different performance characteristics

## 7. Alternative Approach

If the fixes don't work due to deeper API changes, consider using PhysX direct APIs:

```python
# Direct PhysX approach for getting rigid body state
from omni.physx import get_physx_interface

def get_rigid_body_state(prim_path):
    physx = get_physx_interface()
    # Use PhysX APIs to get position, orientation, velocity
    # This bypasses the dynamic control layer
```

## 8. Contributing Back

Once tested and working, consider:
1. Creating a PR to PegasusSimulator repository
2. Documenting any additional changes needed
3. Sharing test results with the community