#!/usr/bin/env python3
import runpy, warnings, sys, inspect


def showwarning(message, category, filename, lineno, file=None, line=None):
    origin_file = filename
    origin_line = lineno
    # Walk stack to find a likely origin frame
    for frame_info in inspect.stack():
        fn = frame_info.filename
        if fn.endswith('run_refactor_with_warnings.py'):
            continue
        if 'warnings' in fn:
            continue
        if fn == '<unknown>':
            continue
        origin_file = fn
        origin_line = frame_info.lineno
        break
    sys.stderr.write(f"{origin_file}:{origin_line}: {category.__name__}: {message}\n")

warnings.showwarning = showwarning

sys.argv = ['src/tools/refactor_external_batch.py', '--limit', '100000']
runpy.run_path('src/tools/refactor_external_batch.py', run_name='__main__')
