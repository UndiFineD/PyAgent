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
p='.secrets.baseline'
with open(p,'r',encoding='utf-8') as f:
    data=json.load(f)
res=data.get('results',{})
paths=set()
for k in res.keys():
    paths.add(k.replace('\\','/'))
out='secrets_paths.txt'
with open(out,'w',encoding='utf-8') as o:
    for p in sorted(paths):
        o.write(p+'\n')
print('Wrote',out,'entries:',len(paths))
print('\nSample:')
for i,p in enumerate(sorted(paths)[:20]):
    print(p)
