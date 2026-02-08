# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_proxyhub.py\proxyhub.py\errors_167365f1132a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-proxyhub\proxyhub\errors.py

"""Errors."""


class ProxyError(Exception):
    pass


class NoProxyError(Exception):
    pass


class ResolveError(Exception):
    pass


class ProxyConnError(ProxyError):
    errmsg = "connection_failed"


class ProxyRecvError(ProxyError):
    errmsg = "connection_is_reset"


class ProxySendError(ProxyError):
    errmsg = "connection_is_reset"


class ProxyTimeoutError(ProxyError):
    errmsg = "connection_timeout"


class ProxyEmptyRecvError(ProxyError):
    errmsg = "empty_response"


class BadStatusError(Exception):  # BadStatusLine
    errmsg = "bad_status"


class BadResponseError(Exception):
    errmsg = "bad_response"


class BadStatusLine(Exception):
    errmsg = "bad_status_line"


class ErrorOnStream(Exception):
    errmsg = "error_on_stream"
