#!/usr/bin/env python3
"""Test the transaction mechanism in rust_core."""
import glob
import os
import shutil
import sys

import rust_core

sys.path.insert(0, os.path.join(os.getcwd(), 'target', 'debug'))
for path in glob.glob(os.path.join(os.getcwd(), 'target', 'debug', '*.dll')):
    shutil.copyfile(path, path[:-4] + '.pyd')
    sys.path.insert(0, os.getcwd())
print('has begin_transaction', hasattr(rust_core, 'begin_transaction'))
print('transaction names', [n for n in dir(rust_core) if 'transaction' in n])
