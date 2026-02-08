# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_brutator.py\lib.py\core.py\exceptions_db9c48992d62.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-web-brutator\lib\core\Exceptions.py

#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# An AuthException will stop the bruteforcing (unexpected error)


class AuthException(Exception):
    pass


# A RequestException might be due to network congestion and will

# stop bruteforcing only after several consecutive similar exceptions


class RequestException(Exception):
    pass
