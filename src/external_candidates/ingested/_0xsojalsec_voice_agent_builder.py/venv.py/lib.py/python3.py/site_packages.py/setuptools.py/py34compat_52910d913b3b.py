# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\setuptools\py34compat.py
import importlib

try:
    import importlib.util
except ImportError:
    pass


try:
    module_from_spec = importlib.util.module_from_spec
except AttributeError:

    def module_from_spec(spec):
        return spec.loader.load_module(spec.name)
