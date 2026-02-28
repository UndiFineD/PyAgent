#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import runpy
import warnings
import sys
import inspect


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
