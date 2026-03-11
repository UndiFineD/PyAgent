#!/usr/bin/env python3
"""Test the key management functions in rust_core."""
import os
import sys

import rust_core

_build_dir = os.path.abspath(os.path.join(os.getcwd(), 'target', 'debug'))
if _build_dir not in sys.path:
    sys.path.insert(0, _build_dir)
if sys.platform.startswith('win'):
    dll = os.path.join(_build_dir, 'rust_core.dll')
    pyd = os.path.join(_build_dir, 'rust_core.pyd')
    if os.path.exists(dll):
        try:
            os.remove(pyd)
        except FileNotFoundError:
            pass
        os.rename(dll, pyd)
try:
    rust_core.clear_keys()
except AttributeError:
    pass

pubpath = 'tempkey.pub'
privpath = 'tempkey.priv'
open(pubpath, 'wb').write(b'x')
open(privpath, 'wb').write(b'y')
rust_core.load_keys(pubpath, privpath)
rust_core.rotate_keys()
print('cwd', os.getcwd())
print('listing', os.listdir())
