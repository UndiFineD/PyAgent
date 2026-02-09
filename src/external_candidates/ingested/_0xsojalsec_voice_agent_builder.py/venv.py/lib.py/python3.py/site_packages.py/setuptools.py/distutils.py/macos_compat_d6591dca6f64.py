# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\setuptools\_distutils\_macos_compat.py
import importlib
import sys


def bypass_compiler_fixup(cmd, args):
    return cmd


if sys.platform == "darwin":
    compiler_fixup = importlib.import_module("_osx_support").compiler_fixup
else:
    compiler_fixup = bypass_compiler_fixup
