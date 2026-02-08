# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wifiphisher.py\wifiphisher.py\common.py\uimethods_a8279a01a008.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wifiphisher\wifiphisher\common\uimethods.py

import importlib

from functools import wraps

import wifiphisher.common.constants


def uimethod(func):
    def _decorator(data, *args, **kwargs):
        response = func(data, *args, **kwargs)

        return response

    func.is_uimethod = True

    return wraps(func)(_decorator)
