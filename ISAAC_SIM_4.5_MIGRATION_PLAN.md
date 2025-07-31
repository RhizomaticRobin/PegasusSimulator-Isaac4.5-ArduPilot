# PegasusSimulator Migration Plan: Isaac Sim 4.2 to 4.5

## Executive Summary

This migration plan details all necessary changes to update PegasusSimulator from Isaac Sim 4.2 to 4.5. The migration involves:
1. **Extension namespace changes** (omni.isaac.* → isaacsim.*)
2. **Core API import updates**
3. **ROS2 bridge modifications**
4. **Dynamic control API adjustments**
5. **ArduPilot interface (STATUS: BROKEN - requires significant rework)**

## 1. Extension Configuration Updates

### File: `extensions/pegasus.simulator/config/extension.toml`
**Line 40:** Replace dependency
```toml
# OLD
"omni.isaac.core" = {}
# NEW
"isaacsim.core.api" = {}
```

## 2. Core Import Changes

### Multiple Example Files Need Updates:

#### Files with `omni.isaac.core.world` imports:
- `examples/0_template_app.py` (line 22)
- `examples/1_px4_single_vehicle.py` (line 22)
- `examples/2_px4_multi_vehicle.py` (line 22)
- `examples/3_ros2_single_vehicle.py` (line 23)
- `examples/4_python_single_vehicle.py` (line 23)
- `examples/5_python_multi_vehicle.py` (line 23)
- `examples/6_paper_results.py` (line 24)
- `examples/8_camera_vehicle.py` (line 23)
- `examples/9_people.py` (line 23)
- `examples/10_graphs.py` (line 23)
- `examples/11_ardupilot_multi_vehicle.py` (line 22)

**Change:**
```python
# OLD
from omni.isaac.core.world import World
# NEW  
from isaacsim.core.api.world import World
```

#### Files with `omni.isaac.core` direct imports:
- `examples/0_template_app.py` (line 22)

**Change:**
```python
# OLD
from omni.isaac.core import World
# NEW
from isaacsim.core.api import World
```

#### Files with `omni.isaac.core.objects` imports:
- `examples/10_graphs.py` (line 24)
- `examples/8_camera_vehicle.py` (line 25)

**Change:**
```python
# OLD
from omni.isaac.core.objects import DynamicCuboid
# NEW
from isaacsim.core.api.objects import DynamicCuboid
```

## 3. Dynamic Control API Changes

### Files: 
- `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py` (line 21)
- `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py` (line 10)

**Change:**
```python
# OLD
from omni.isaac.dynamic_control import _dynamic_control
# NEW  
from isaacsim.core.dynamic_control import _dynamic_control
```

## 4. Sensor API Changes

### Files:
- `extensions/pegasus.simulator/pegasus/simulator/logic/graphs/ros2_camera_graph.py` (line 13)
- `extensions/pegasus.simulator/pegasus/simulator/logic/graphical_sensors/monocular_camera.py` (line 13)

**Change:**
```python
# OLD
from omni.isaac.sensor import Camera
# NEW
from isaacsim.sensors.camera import Camera
```

## 5. Core Utilities Updates

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py` (line 18)
**Change:**
```python
# OLD
from isaacsim.core.utils.prims import define_prim, get_prim_at_path
# NEW
from isaacsim.core.utils.prims import define_prim, get_prim_at_path
```

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py` (line 20)
**Change:**
```python
# OLD
from isaacsim.core.api.robots.robot import Robot
# NEW
from isaacsim.core.api.robots.robot import Robot
```

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/interface/pegasus_interface.py`
**Lines 20-22:** Update imports
```python
# OLD
from isaacsim.core.api.world import World
from isaacsim.core.utils.stage import clear_stage, create_new_stage_async, update_stage_async, create_new_stage
from isaacsim.core.utils.viewports import set_camera_view
# NEW
from isaacsim.core.api.world import World
from isaacsim.core.utils.stage import clear_stage, create_new_stage_async, update_stage_async, create_new_stage
from isaacsim.core.utils.viewports import set_camera_view
```

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/interface/pegasus_interface.py` (line 23)
**Change:**
```python
# OLD
import isaacsim.storage.native as nucleus
# NEW
import isaacsim.storage.native as nucleus
```

## 6. People Extension Updates

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/people/person.py`
**Lines 19, 24-26:** Update imports
```python
# OLD
from isaacsim.storage.native import get_assets_root_path
from isaacsim.replicator.agent.core.settings import PrimPaths
from isaacsim.replicator.agent.core.stage_util import CharacterUtil
from isaacsim.replicator.agent.core.simulation import SimulationManager
# NEW
from isaacsim.storage.native import get_assets_root_path
from isaacsim.replicator.agent.core.settings import PrimPaths
from isaacsim.replicator.agent.core.stage_util import CharacterUtil
from isaacsim.replicator.agent.core.simulation import SimulationManager
```

## 7. ROS2 Backend Updates

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/backends/ros2_backend.py`
**Line 10:** Update extension enable
```python
# OLD
enable_extension("isaacsim.ros2.bridge")
# NEW
enable_extension("isaacsim.ros2.bridge")
```

**Line 36:** Update camera info import
```python
# OLD
from isaacsim.ros2.bridge import read_camera_info
# NEW
from isaacsim.ros2.bridge import read_camera_info
```

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/people_backends/ros2_people_backend.py` (line 13)
**Change:**
```python
# OLD
from isaacsim.core.utils.extensions import enable_extension
# NEW
from isaacsim.core.utils.extensions import enable_extension
```

### File: `extensions/pegasus.simulator/pegasus/simulator/logic/graphs/ros2_camera_graph.py`
**Lines 9, 11-12:** Update imports
```python
# OLD
from isaacsim.core.utils import stage
from isaacsim.core.utils.prims import is_prim_path_valid
from isaacsim.core.utils.prims import set_targets
# NEW
from isaacsim.core.utils import stage
from isaacsim.core.utils.prims import is_prim_path_valid
from isaacsim.core.utils.prims import set_targets
```

## 8. Debug Draw Updates

### Files:
- `examples/5_python_multi_vehicle.py` (line 46)
- `examples/6_paper_results.py` (line 49)

**Change:**
```python
# OLD
from isaacsim.util.debug_draw import _debug_draw
# NEW
from isaacsim.util.debug_draw import _debug_draw
```

## 9. ArduPilot Interface (CRITICAL - BROKEN)

### **WARNING**: The ArduPilot interface is **NOT TESTED** in Isaac Sim 4.5.0 and likely broken!

### Affected Files:
- `extensions/pegasus.simulator/pegasus/simulator/logic/backends/ardupilot_mavlink_backend.py`
- `extensions/pegasus.simulator/pegasus/simulator/logic/backends/tools/ardupilot_launch_tool.py`
- All UI files that reference ArduPilot functionality

### Required Changes:
1. **Sensor APIs** - Unknown new locations for IMU, GPS, Barometer, Magnetometer
2. **Coordinate System Transforms** - May need adjustment due to physics changes
3. **MAVLINK Communication** - Timing synchronization likely affected
4. **Dynamic Control** - API changes affect vehicle control

### Recommendation:
**DO NOT MIGRATE** if ArduPilot functionality is required. Wait for official update or contribute fixes.

## 10. Migration Script

Save this as `migrate_to_isaac_4.5.py`:

```python
#!/usr/bin/env python3
"""
PegasusSimulator Migration Script for Isaac Sim 4.2 to 4.5
"""

import os
import re
import shutil
from pathlib import Path

# Define replacements
REPLACEMENTS = [
    # Core imports
    (r'from omni\.isaac\.core\.world import World', 'from isaacsim.core.api.world import World'),
    (r'from omni\.isaac\.core import World', 'from isaacsim.core.api import World'),
    (r'from omni\.isaac\.core\.objects import', 'from isaacsim.core.api.objects import'),
    
    # Dynamic control
    (r'from omni\.isaac\.dynamic_control import', 'from isaacsim.core.dynamic_control import'),
    
    # Sensors
    (r'from omni\.isaac\.sensor import Camera', 'from isaacsim.sensors.camera import Camera'),
    
    # Extension dependencies
    (r'"omni\.isaac\.core"\s*=\s*\{\}', '"isaacsim.core.api" = {}'),
    
    # ROS2 bridge
    (r'enable_extension\("isaacsim\.ros2\.bridge"\)', 'enable_extension("isaacsim.ros2.bridge")'),
]

def migrate_file(filepath):
    """Migrate a single file"""
    print(f"Processing: {filepath}")
    
    # Backup original
    backup_path = filepath + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(filepath, backup_path)
    
    # Read content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply replacements
    original_content = content
    for old_pattern, new_pattern in REPLACEMENTS:
        content = re.sub(old_pattern, new_pattern, content)
    
    # Write if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated {filepath}")
    else:
        print(f"  - No changes needed for {filepath}")

def main():
    # Find PegasusSimulator root
    pegasus_root = Path(__file__).parent
    
    print("PegasusSimulator Migration Script")
    print("=================================")
    print(f"Root directory: {pegasus_root}")
    print()
    
    # Files to migrate
    files_to_migrate = [
        # Examples
        "examples/0_template_app.py",
        "examples/1_px4_single_vehicle.py",
        "examples/2_px4_multi_vehicle.py",
        "examples/3_ros2_single_vehicle.py",
        "examples/4_python_single_vehicle.py",
        "examples/5_python_multi_vehicle.py",
        "examples/6_paper_results.py",
        "examples/8_camera_vehicle.py",
        "examples/9_people.py",
        "examples/10_graphs.py",
        "examples/11_ardupilot_multi_vehicle.py",
        
        # Core files
        "extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/interface/pegasus_interface.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/backends/ros2_backend.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/people_backends/ros2_people_backend.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/people/person.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/graphs/ros2_camera_graph.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/graphical_sensors/monocular_camera.py",
        
        # Config
        "extensions/pegasus.simulator/config/extension.toml",
    ]
    
    # Migrate files
    for file_path in files_to_migrate:
        full_path = pegasus_root / file_path
        if full_path.exists():
            migrate_file(full_path)
        else:
            print(f"  ⚠ File not found: {file_path}")
    
    print("\nMigration complete!")
    print("\n⚠️  WARNING: ArduPilot interface is NOT tested and likely broken!")
    print("Please test thoroughly before using in production.")

if __name__ == "__main__":
    main()
```

## 11. Testing Checklist

After migration, test the following:

1. [ ] Basic simulator launch
2. [ ] PX4 single vehicle example
3. [ ] PX4 multi-vehicle example
4. [ ] Python control backend examples
5. [ ] ROS2 backend functionality
6. [ ] Camera and sensor integration
7. [ ] People simulation (if used)
8. [ ] **ArduPilot backend** (EXPECTED TO FAIL)

## 12. Rollback Plan

If migration fails:
1. Restore all `.bak` files created by the migration script
2. Revert to Isaac Sim 4.2.0
3. Use PegasusSimulator v4.2.0 tag

## Notes

- The migration script creates `.bak` files for all modified files
- Manual verification recommended for critical functionality
- ArduPilot users should NOT migrate until fixes are available
- Consider contributing ArduPilot fixes back to the project