# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\setuptools\_distutils\py38compat.py
def aix_platform(osname, version, release):
    try:
        import _aix_support

        return _aix_support.aix_platform()
    except ImportError:
        pass
    return "{}-{}.{}".format(osname, version, release)
