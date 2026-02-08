# Refactored by Copilot placeholder
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\run_module\run_gcp_module.py
# NOTE: extracted with static-only rules; review before use


def run_gcp_module(imported_module, all_sessions, cred_prof, workspace, useragent=""):
    if imported_module.needs_creds:
        return {"message": "You ran a GCP module"}

    else:
        return imported_module.exploit()
