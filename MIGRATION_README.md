# PegasusSimulator Isaac Sim 4.5 Migration

This folder contains migration tools and documentation for updating PegasusSimulator from Isaac Sim 4.2 to 4.5.

## Files

1. **ISAAC_SIM_4.5_MIGRATION_PLAN.md** - Comprehensive migration plan with all required changes
2. **migrate_to_isaac_4.5.py** - Automated migration script

## Quick Start

### 1. Review the Migration Plan
```bash
cat ISAAC_SIM_4.5_MIGRATION_PLAN.md
```

### 2. Test Migration (Dry Run)
```bash
python migrate_to_isaac_4.5.py --dry-run
```

### 3. Apply Migration
```bash
python migrate_to_isaac_4.5.py
```

### 4. Restore from Backup (if needed)
```bash
# The script creates .bak files for all modified files
# To restore a single file:
mv file.py.bak file.py

# To restore all files:
find . -name "*.bak" -exec sh -c 'mv "$0" "${0%.bak}"' {} \;
```

## Script Options

- `--dry-run` - Show what would be changed without modifying files
- `--no-backup` - Skip creating backup files (not recommended)
- `--root PATH` - Specify PegasusSimulator root directory (default: current directory)

## Important Notes

⚠️ **WARNING**: ArduPilot functionality is **BROKEN** in Isaac Sim 4.5.0
- The ArduPilot backend has NOT been tested with Isaac Sim 4.5
- Sensor APIs and coordinate transformations likely need updates
- If you need ArduPilot, stay on Isaac Sim 4.2 with PegasusSimulator 4.2.0

## Testing After Migration

1. Basic simulator launch
2. PX4 examples (should work)
3. Python control examples (should work)
4. ROS2 backend (should work)
5. ArduPilot examples (expected to FAIL)

## Support

For issues or questions:
- Check the official PegasusSimulator repository
- Review the migration plan for manual fixes
- Consider contributing ArduPilot fixes back to the project