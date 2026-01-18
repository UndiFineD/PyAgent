import os
path = r'c:\DEV\PyAgent\src\infrastructure\attention\PagedAttentionEngine.py'
with open(path, 'w') as f:
    f.write('# SPDX-License-Identifier: Apache-2.0\n')
    f.write('\"\"\"\n')
    f.write('Paged Attention Engine wrapper.\n')
    f.write('Original monolithic file split into the paged_attention subpackage.\n')
    f.write('\"\"\"\n\n')
    f.write('from .paged_attention import *\n')
print(f'Overwrote {path}')
