# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\dttm_711486ac4244.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\dttm.py

from datetime import datetime, timezone

def current_datetime() -> datetime:

    return datetime.now()

def current_datetime_utc() -> datetime:

    return datetime.now(timezone.utc)

def current_datetime_utc_str() -> str:

    return current_datetime_utc().strftime("%Y-%m-%dT%H:%M:%S")

