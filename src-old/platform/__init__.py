"""Safe platform shim that delegates to the stdlib's platform.py when available.
Avoids recursion by loading the stdlib implementation directly from the stdlib path.
If the stdlib platform module is not found, provides a minimal fallback for tests.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import sysconfig


def _load_stdlib_platform():
    stdlib_dir = sysconfig.get_path("stdlib")
    if not stdlib_dir:
        return None
    platform_path = os.path.join(stdlib_dir, "platform.py")
    if not os.path.exists(platform_path):
        return None
    spec = importlib.util.spec_from_file_location("_stdlib_platform", platform_path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_stdlib_platform = _load_stdlib_platform()

if _stdlib_platform is not None:
    # re-export public symbols from the stdlib platform module
    for _name in dir(_stdlib_platform):
        if _name.startswith("_"):
            continue
        globals()[_name] = getattr(_stdlib_platform, _name)
else:
    # Minimal fallbacks used when stdlib platform can't be loaded
    def python_implementation():
        return sys.implementation.name if hasattr(sys, "implementation") else "CPython"

    def python_version():
        return sys.version.split(" ")[0]

    def system():
        return os.name

    def node():
        try:
            return os.uname().nodename
        except Exception:
            return os.getenv("COMPUTERNAME", "")

__all__ = [name for name in globals().keys() if not name.startswith("_")]
"""Project `platform` package shim.

This package exposes project-local `platform` submodules under
`src/infrastructure/services/platform` while delegating attribute access
to the stdlib `platform` module when appropriate.
"""
from collections import namedtuple

# Ensure Python will find package submodules under project src path
_repo_root = os.path.dirname(os.path.dirname(__file__))
_candidate = os.path.join(_repo_root, "src", "infrastructure", "services", "platform")
if os.path.isdir(_candidate):
    __path__.insert(0, _candidate)

# Try to load the standard-library `platform` module from the stdlib path
_stdlib = None
try:
    _stdlib_path = os.path.join(sysconfig.get_paths()["stdlib"], "platform.py")
    if os.path.exists(_stdlib_path):
        spec = importlib.util.spec_from_file_location("_stdlib_platform", _stdlib_path)
        _stdlib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_stdlib)
except Exception:
    _stdlib = None

# Provide lightweight fallbacks and delegate to stdlib when available
_Uname = namedtuple("_Uname", ["system", "node", "release", "version", "machine"])

def system():
    if _stdlib and hasattr(_stdlib, "system"):
        return _stdlib.system()
    import os as _os
    return "Windows" if _os.name == "nt" else _os.name

def machine():
    if _stdlib and hasattr(_stdlib, "machine"):
        return _stdlib.machine()
    import os as _os
    return _os.environ.get("PROCESSOR_ARCHITECTURE", "x86_64")

def uname():
    if _stdlib and hasattr(_stdlib, "uname"):
        return _stdlib.uname()
    return _Uname(system(), "localhost", "0", "0", machine())

def python_version():
    if _stdlib and hasattr(_stdlib, "python_version"):
        return _stdlib.python_version()
    import sys as _sys
    return _sys.version.split()[0]

def __getattr__(name: str):
    if _stdlib and hasattr(_stdlib, name):
        return getattr(_stdlib, name)
    raise AttributeError(name)

def __dir__():
    names = list(globals().keys())
    if _stdlib:
        names += [n for n in dir(_stdlib) if not n.startswith("_")]
    return sorted(set(names))

__all__ = ["system", "machine", "uname", "python_version"]
