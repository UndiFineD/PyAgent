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
