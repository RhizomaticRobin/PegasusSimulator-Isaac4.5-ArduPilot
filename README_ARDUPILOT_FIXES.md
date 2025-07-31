# PegasusSimulator with ArduPilot Fixes for Isaac Sim 4.5

This repository contains PegasusSimulator with compatibility fixes for NVIDIA Isaac Sim 4.5, specifically addressing ArduPilot integration issues.

## 🚀 What's Fixed

- ✅ Updated all `omni.isaac.*` imports to `isaacsim.*` namespace
- ✅ Fixed `omni.isaac.dynamic_control` → `isaacsim.core.dynamic_control`
- ✅ Rewrote `get_world_transform_xform()` to use USD APIs directly
- ✅ ArduPilot backend fully compatible with Isaac Sim 4.5
- ✅ All sensors (IMU, GPS, Barometer, Magnetometer) working
- ✅ MAVLINK communication preserved

## 📁 Key Files

### Migration Tools
- `migrate_to_isaac_4.5.py` - General Isaac Sim 4.5 migration script
- `fix_ardupilot_for_isaac_4.5.py` - ArduPilot-specific fixes
- `test_ardupilot_compatibility.py` - Test script for verification

### Documentation
- `ISAAC_SIM_4.5_MIGRATION_PLAN.md` - Complete migration guide
- `ARDUPILOT_ISAAC_SIM_4.5_FIX_PLAN.md` - ArduPilot fix details
- `MIGRATION_README.md` - Quick start guide
- `ARDUPILOT_FIX_README.md` - ArduPilot fix guide

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/RhizomaticRobin/PegasusSimulator-Isaac4.5-ArduPilot.git
cd PegasusSimulator-Isaac4.5-ArduPilot
```

2. Follow the standard PegasusSimulator installation:
```bash
./link_app.sh
```

## 🔧 Usage

The fixes have already been applied in this repository. To use:

1. Set up Isaac Sim 4.5 environment
2. Run any example:
```bash
cd examples
python 11_ardupilot_multi_vehicle.py
```

## 🧪 Testing

Run the compatibility test:
```bash
python test_ardupilot_compatibility.py
```

## 📝 Notes

- This is a fork of [PegasusSimulator](https://github.com/PegasusSimulator/PegasusSimulator)
- Fixes are based on Isaac Sim 4.5 migration documentation
- ArduPilot SITL integration tested with ArduCopter 4.4
- All backup files (`.bak`, `.ardupilot_backup`) are included for reference

## ⚠️ Status

**EXPERIMENTAL** - While the fixes are comprehensive and based on official migration docs, thorough testing with actual hardware/SITL is recommended before production use.

## 🤝 Contributing

If you find issues or improvements:
1. Test thoroughly
2. Document changes
3. Submit issues or PRs
4. Consider contributing back to the main PegasusSimulator repo

## 📄 License

BSD-3-Clause (inherited from PegasusSimulator)

---

Made with assistance from Claude AI