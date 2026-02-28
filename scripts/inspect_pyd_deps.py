#!/usr/bin/env python3
import os
import sys
try:
    import pefile
except Exception as e:
    print('ERROR: pefile not installed:', e, file=sys.stderr)
    sys.exit(2)

pyd = r'C:\Dev\PyAgent\\.venv3.13\\Lib\\site-packages\\rust_core\\rust_core.cp313-win_amd64.pyd'
if not os.path.exists(pyd):
    print('ERROR: .pyd not found at', pyd, file=sys.stderr)
    sys.exit(3)

pe = pefile.PE(pyd)
imports = [entry.dll.decode('utf-8') for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', [])]
print('Inspecting', pyd)
print('Imported DLLs (count=%d):' % len(imports))
for d in imports:
    print('  -', d)

# Search for each DLL in common locations
search_paths = []
windir = os.environ.get('windir') or os.environ.get('WINDIR') or r'C:\Windows'
search_paths.append(os.path.join(windir, 'System32'))
search_paths.append(os.path.join(windir, 'SysWOW64'))
# add exe dir
search_paths.append(os.path.dirname(pyd))
# add PATH entries
path_env = os.environ.get('PATH','')
for p in path_env.split(';'):
    if p:
        search_paths.append(p)

print('\nSearching for DLLs in System32, SysWOW64, .pyd dir and PATH...')
missing = []
for d in imports:
    found = False
    for sp in search_paths:
        try:
            full = os.path.join(sp, d)
        except Exception:
            continue
        if os.path.exists(full):
            print(f"FOUND: {d} -> {full}")
            found = True
            break
    if not found:
        print(f"MISSING: {d}")
        missing.append(d)

print('\nSummary:')
print('Missing count:', len(missing))
for m in missing:
    print('  *', m)

if missing:
    sys.exit(1)
else:
    sys.exit(0)
