#!/usr/bin/env python
"""A simple Python launcher that mimics the behavior of the Windows Launcher (py.exe) for testing purposes."""
import sys
import os
import subprocess


args = sys.argv[1:]
filtered = []
i = 0
while i < len(args):
    a = args[i]
    # Strip version-selector flags that the real Windows Launcher would handle via registry
    if a.startswith('-') and len(a) > 1 and a[1:].replace('.', '').replace('-', '').isdigit():
        i += 1
        continue
    if a in ('-3', '-2', '-', '-0'):
        i += 1
        continue
    filtered.append(a)
    i += 1

# When frozen by PyInstaller, sys.executable is this exe
# — find python.exe in same directory
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    python = os.path.join(exe_dir, 'python.exe')
    if not os.path.isfile(python):
        # Fallback: search PATH for python.exe (not py.exe)
        import shutil
        python = shutil.which('python') or shutil.which('python3') or 'python'
else:
    python = sys.executable

result = subprocess.run([python] + filtered)
sys.exit(result.returncode)
