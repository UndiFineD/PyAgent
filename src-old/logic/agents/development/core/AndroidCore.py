
r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/development/core/AndroidCore.description.md

# AndroidCore

**File**: `src\\logic\agents\\development\\core\\AndroidCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 66  
**Complexity**: 3 (simple)

## Overview

Core logic for Android ADB integration (Phase 175).
Encapsulates ADB commands for UI testing.

## Classes (1)

### `AndroidCore`

Class AndroidCore implementation.

**Methods** (3):
- `run_adb_command(command, serial, recorder)`
- `list_devices(recorder)`
- `take_screenshot(output_path, serial, recorder)`

## Dependencies

**Imports** (4):
- `src.core.base.interfaces.ContextRecorderInterface`
- `subprocess`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/core/AndroidCore.improvements.md

# Improvements for AndroidCore

**File**: `src\\logic\agents\\development\\core\\AndroidCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 66 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: AndroidCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AndroidCore_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Core logic for Android ADB integration (Phase 175).
Encapsulates ADB commands for UI testing.
"""

import subprocess

from src.core.base.interfaces import ContextRecorderInterface


class AndroidCore:
    @staticmethod
    def run_adb_command(command: list[str], serial: str | None = None, recorder: ContextRecorderInterface | None = None) -> str:
        """Runs an adb command and returns the output.
        """
        base = ["adb"]
        if serial:
            base.extend(["-s", serial])

        full_command = base + command
        try:
            result = subprocess.run(full_command, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr.strip()}"
        except FileNotFoundError:
            output = "Error: adb not found in PATH."

        if recorder:
            recorder.record_interaction(
                provider="android",
                model="adb",
                prompt=" ".join(full_command),
                result=output[:5000],
                meta={"serial": serial}
            )

        return output

    @staticmethod
    def list_devices(recorder: ContextRecorderInterface | None = None) -> list[str]:
        """Returns a list of connected device serials.
        """
        output = AndroidCore.run_adb_command(["devices"], recorder=recorder)
        lines = output.splitlines()
        devices = []
        for line in lines[1:]: # Skip "List of devices attached"
            if "device" in line and "offline" not in line:
                devices.append(line.split()[0])
        return devices

    @staticmethod
    def take_screenshot(output_path: str, serial: str | None = None, recorder: ContextRecorderInterface | None = None) -> bool:
        """Takes a screenshot of the device.
        """
        # Take screenshot on device
        res = AndroidCore.run_adb_command(["shell", "screencap", "-p", "/sdcard/screen.png"], serial, recorder)
        if "Error" in res:
            return False
        # Pull to host
        res = AndroidCore.run_adb_command(["pull", "/sdcard/screen.png", output_path], serial, recorder)
        return "Error" not in res
