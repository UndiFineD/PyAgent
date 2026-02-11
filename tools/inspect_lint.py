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

import json
p='lint_results.json'
with open(p,'r',encoding='utf-8') as f:
    d=json.load(f)
first=d[0]
print('keys:', list(first.keys()))
print('ruff present:', 'ruff' in first)
print('ruff type:', type(first['ruff']))
print('ruff exit_code repr:', repr(first['ruff'].get('exit_code')))
print('ruff stdout repr:', repr(first['ruff'].get('stdout')))
