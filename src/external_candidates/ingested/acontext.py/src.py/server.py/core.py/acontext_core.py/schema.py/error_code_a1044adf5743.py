# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\error_code.py
from enum import IntEnum


class Code(IntEnum):
    SUCCESS = 200

    # Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    # Server Errors
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503

    LLM_READABLE_ERROR = 10001
