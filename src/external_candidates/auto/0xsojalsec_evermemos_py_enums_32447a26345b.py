# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\authorize.py\enums_32447a26345b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\authorize\enums.py

from enum import Enum

class Role(Enum):

    """User role enumeration"""

    ANONYMOUS = "anonymous"  # Anonymous user

    USER = "user"  # Regular user

    ADMIN = "admin"  # Administrator

    SIGNATURE = "signature"  # HMAC signature verification user

