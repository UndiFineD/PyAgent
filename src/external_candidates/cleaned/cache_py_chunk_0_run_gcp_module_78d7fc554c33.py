# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_run_gcp_module_78d7fc554c33.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_run_gcp_module.py

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\run_module\run_gcp_module.py

# NOTE: extracted with static-only rules; review before use


def run_gcp_module(imported_module, all_sessions, cred_prof, workspace, useragent=""):
    if imported_module.needs_creds:
        return {"message": "You ran a GCP module"}

    else:
        return imported_module.exploit()
