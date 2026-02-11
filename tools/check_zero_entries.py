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

from pathlib import Path
text = Path('lint_results.json').read_text(encoding='utf-8')
count = text.count('"exit_code": 0')
print('count_exit_code_0=', count)
# Print small context samples if any
if count:
    idx = text.find('"exit_code": 0')
    start = max(0, idx-200)
    end = min(len(text), idx+200)
    print(text[start:end])
else:
    print('none found')
