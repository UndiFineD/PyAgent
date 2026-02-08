# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\error_code_a1044adf5743.py
# NOTE: extracted with static-only rules; review before use

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
