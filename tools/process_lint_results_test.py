#!/usr/bin/env python3
import json
import subprocess
import sys
import os

LINT_JSON = os.path.join('temp','lint_results.json')
PYTHON = os.path.join('.venv','Scripts','python.exe') if os.path.isdir('.venv') else sys.executable

def run(cmd):
    return subprocess.run(cmd, shell=False, capture_output=True, text=True)

with open(LINT_JSON,'r',encoding='utf-8') as f:
    entries = json.load(f)

remaining = []
removed = []
for e in entries:
    path = e.get('file')
    if not path:
        continue
    norm = path.replace('\\','/')
    # run autopep8
    print('Formatting', norm)
    r = run([PYTHON, '-m', 'autopep8', '--in-place', '--aggressive', '--aggressive', '--max-line-length', '120', norm])
    if r.returncode != 0:
        print('autopep8 failed on', norm, r.stderr)
    # run flake8
    fproc = run([PYTHON, '-m', 'flake8', norm])
    if fproc.returncode == 0 and not fproc.stdout:
        removed.append(norm)
        print('No flake8 issues:', norm)
    else:
        remaining.append(e)
        print('Still issues for', norm)

with open(LINT_JSON,'w',encoding='utf-8') as f:
    json.dump(remaining,f,indent=2)

print('Removed', len(removed), 'entries;', len(remaining), 'remain')
