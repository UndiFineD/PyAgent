#!/usr/bin/env python3
import os
from pathlib import Path

test_path = '/home/runner/work/PyAgent/PyAgent/C:\\DEV\\PyAgent\\'
alt = r'C:\\DEV\\PyAgent\\'
cur = '.'

prefix = '/home/runner/work/PyAgent/PyAgent/'

def normalize(p):
    if p.startswith(prefix):
        p = p[len(prefix):]
    # Replace forward slashes with OS separator
    p = p.replace('/', os.sep)
    # Strip surrounding quotes and whitespace
    p = p.strip()
    if p == '':
        return os.path.normpath('.')
    return os.path.normpath(p)

np = normalize(test_path)
na = normalize(alt)
nc = normalize(cur)

print('original_test_path:', test_path)
print('normalized_test_path:', np)
print('alt_path:', alt)
print('normalized_alt_path:', na)
print('dot path normalized:', nc)
print()
print('equals alt?:', os.path.normcase(np) == os.path.normcase(na))
print('equals dot?:', os.path.normcase(np) == os.path.normcase(nc))
print()
print('exists(normalized_test_path):', Path(np).exists())
print('exists(normalized_alt_path):', Path(na).exists())
print('exists(dot):', Path(nc).exists())
