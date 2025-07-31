#!/usr/bin/env python3
"""
PegasusSimulator Migration Script for Isaac Sim 4.2 to 4.5
Automatically updates imports and dependencies for Isaac Sim 4.5.0
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Define replacements for Python files
PYTHON_REPLACEMENTS = [
    # Core World imports
    (r'from omni\.isaac\.core\.world import World', 'from isaacsim.core.api.world import World'),
    (r'from omni\.isaac\.core import World', 'from isaacsim.core.api import World'),
    
    # Core objects
    (r'from omni\.isaac\.core\.objects import', 'from isaacsim.core.api.objects import'),
    
    # Dynamic control
    (r'from omni\.isaac\.dynamic_control import', 'from isaacsim.core.dynamic_control import'),
    
    # Sensors
    (r'from omni\.isaac\.sensor import Camera', 'from isaacsim.sensors.camera import Camera'),
    
    # Note: Already migrated imports (isaacsim.*) are left as-is since they follow new pattern
]

# Define replacements for TOML files
TOML_REPLACEMENTS = [
    (r'"omni\.isaac\.core"\s*=\s*\{\}', '"isaacsim.core.api" = {}'),
]

# Files to migrate
FILES_TO_MIGRATE = {
    'python': [
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
        
        # Core vehicle files
        "extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/vehicle.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/vehicles/multirotor.py",
        
        # Interface files
        "extensions/pegasus.simulator/pegasus/simulator/logic/interface/pegasus_interface.py",
        
        # Backend files
        "extensions/pegasus.simulator/pegasus/simulator/logic/backends/ros2_backend.py",
        "extensions/pegasus.simulator/pegasus/simulator/logic/people_backends/ros2_people_backend.py",
        
        # People files
        "extensions/pegasus.simulator/pegasus/simulator/logic/people/person.py",
        
        # Graph files
        "extensions/pegasus.simulator/pegasus/simulator/logic/graphs/ros2_camera_graph.py",
        
        # Sensor files
        "extensions/pegasus.simulator/pegasus/simulator/logic/graphical_sensors/monocular_camera.py",
    ],
    'toml': [
        "extensions/pegasus.simulator/config/extension.toml",
    ]
}

# ArduPilot files that need manual attention
ARDUPILOT_FILES = [
    "extensions/pegasus.simulator/pegasus/simulator/logic/backends/ardupilot_mavlink_backend.py",
    "extensions/pegasus.simulator/pegasus/simulator/logic/backends/tools/ardupilot_launch_tool.py",
]

class MigrationTool:
    def __init__(self, root_path=None, dry_run=False, no_backup=False):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.dry_run = dry_run
        self.no_backup = no_backup
        self.changes_made = []
        self.warnings = []
        
    def backup_file(self, filepath):
        """Create a backup of the file"""
        if self.no_backup or self.dry_run:
            return
            
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        if not backup_path.exists():
            shutil.copy2(filepath, backup_path)
            print(f"  📋 Backed up to: {backup_path.name}")
    
    def migrate_python_file(self, filepath):
        """Migrate a Python file"""
        print(f"\n🔧 Processing: {filepath.relative_to(self.root_path)}")
        
        # Read content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            return
        
        # Apply replacements
        original_content = content
        changes = []
        
        for old_pattern, new_pattern in PYTHON_REPLACEMENTS:
            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_pattern, content)
                changes.append(f"    • {matches[0]} → {new_pattern}")
        
        # Check for ArduPilot references
        if 'ardupilot' in content.lower() or 'ArduPilot' in content:
            self.warnings.append(filepath)
        
        # Write if changed
        if content != original_content:
            if not self.dry_run:
                self.backup_file(filepath)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"  ✅ Updated with {len(changes)} changes:")
            for change in changes:
                print(change)
            self.changes_made.append(filepath)
        else:
            print(f"  ⏭️  No changes needed")
    
    def migrate_toml_file(self, filepath):
        """Migrate a TOML file"""
        print(f"\n🔧 Processing: {filepath.relative_to(self.root_path)}")
        
        # Read content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            return
        
        # Apply replacements
        original_content = content
        changes = []
        
        for old_pattern, new_pattern in TOML_REPLACEMENTS:
            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_pattern, content)
                changes.append(f"    • {old_pattern} → {new_pattern}")
        
        # Write if changed
        if content != original_content:
            if not self.dry_run:
                self.backup_file(filepath)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"  ✅ Updated with {len(changes)} changes:")
            for change in changes:
                print(change)
            self.changes_made.append(filepath)
        else:
            print(f"  ⏭️  No changes needed")
    
    def run_migration(self):
        """Run the complete migration"""
        print("=" * 60)
        print("PegasusSimulator Migration Tool - Isaac Sim 4.2 → 4.5")
        print("=" * 60)
        print(f"Root directory: {self.root_path}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Backup: {'DISABLED' if self.no_backup else 'ENABLED'}")
        print()
        
        # Process Python files
        print("📄 Processing Python files...")
        for file_path in FILES_TO_MIGRATE['python']:
            full_path = self.root_path / file_path
            if full_path.exists():
                self.migrate_python_file(full_path)
            else:
                print(f"\n⚠️  File not found: {file_path}")
        
        # Process TOML files
        print("\n📄 Processing TOML files...")
        for file_path in FILES_TO_MIGRATE['toml']:
            full_path = self.root_path / file_path
            if full_path.exists():
                self.migrate_toml_file(full_path)
            else:
                print(f"\n⚠️  File not found: {file_path}")
        
        # Summary
        print("\n" + "=" * 60)
        print("Migration Summary")
        print("=" * 60)
        print(f"✅ Files modified: {len(self.changes_made)}")
        
        if self.warnings:
            print(f"\n⚠️  Files with ArduPilot references ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"    • {warning.relative_to(self.root_path)}")
        
        print(f"\n🚨 ArduPilot files requiring manual attention:")
        for ardupilot_file in ARDUPILOT_FILES:
            full_path = self.root_path / ardupilot_file
            if full_path.exists():
                print(f"    • {ardupilot_file}")
        
        if self.dry_run:
            print("\n📝 This was a DRY RUN - no files were modified")
            print("    Run without --dry-run to apply changes")
        else:
            print("\n✅ Migration complete!")
            print("    Backup files created with .bak extension")
        
        print("\n⚠️  IMPORTANT WARNINGS:")
        print("    1. ArduPilot interface is NOT tested in Isaac Sim 4.5.0")
        print("    2. Test all functionality before production use")
        print("    3. Manual verification recommended for critical features")

def main():
    parser = argparse.ArgumentParser(
        description="Migrate PegasusSimulator from Isaac Sim 4.2 to 4.5"
    )
    parser.add_argument(
        "--root", 
        type=str, 
        help="Root directory of PegasusSimulator (default: current directory)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be changed without modifying files"
    )
    parser.add_argument(
        "--no-backup", 
        action="store_true",
        help="Skip creating backup files"
    )
    
    args = parser.parse_args()
    
    # Create migration tool
    tool = MigrationTool(
        root_path=args.root,
        dry_run=args.dry_run,
        no_backup=args.no_backup
    )
    
    # Run migration
    tool.run_migration()

if __name__ == "__main__":
    main()