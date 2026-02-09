# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\authorize\enums.py
from enum import Enum


class Role(Enum):
    """User role enumeration"""

    ANONYMOUS = "anonymous"  # Anonymous user
    USER = "user"  # Regular user
    ADMIN = "admin"  # Administrator
    SIGNATURE = "signature"  # HMAC signature verification user
