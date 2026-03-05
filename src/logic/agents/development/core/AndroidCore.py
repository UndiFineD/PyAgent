
"""
Core logic for Android ADB integration (Phase 175).
Encapsulates ADB commands for UI testing.
"""

import subprocess
from typing import List, Optional

from src.core.base.interfaces import ContextRecorderInterface

class AndroidCore:
    @staticmethod
    def run_adb_command(command: list[str], serial: str | None = None, recorder: ContextRecorderInterface | None = None) -> str:
        """
        Runs an adb command and returns the output.
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
        """
        Returns a list of connected device serials.
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
        """
        Takes a screenshot of the device.
        """
        # Take screenshot on device
        res = AndroidCore.run_adb_command(["shell", "screencap", "-p", "/sdcard/screen.png"], serial, recorder)
        if "Error" in res:
            return False
        # Pull to host
        res = AndroidCore.run_adb_command(["pull", "/sdcard/screen.png", output_path], serial, recorder)
        return "Error" not in res