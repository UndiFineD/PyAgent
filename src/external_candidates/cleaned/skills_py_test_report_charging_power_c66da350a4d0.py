# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\officialpm.py\my_tesla.py\tests.py\test_report_charging_power_c66da350a4d0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\officialpm\my-tesla\tests\test_report_charging_power.py

import sys

import unittest

from pathlib import Path

# Allow importing scripts/tesla.py as a module

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class ReportChargingPowerTests(unittest.TestCase):
    def test_report_includes_charging_power_details_when_present(self):
        vehicle = {"display_name": "Test Car", "state": "online"}

        data = {
            "charge_state": {
                "battery_level": 50,
                "battery_range": 123.4,
                "charging_state": "Charging",
                "charger_power": 7,
                "charger_voltage": 240,
                "charger_actual_current": 30,
            },
            "climate_state": {},
            "vehicle_state": {},
        }

        out = tesla._report(vehicle, data)

        self.assertIn("Charging: Charging", out)

        self.assertIn("Charging power:", out)

        self.assertIn("7 kW", out)

        self.assertIn("240V", out)

        self.assertIn("30A", out)


if __name__ == "__main__":
    unittest.main()
