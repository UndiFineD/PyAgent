#!/usr/bin/env python3
import os,re
root = os.getcwd()
matches=[]
for dirpath,dirnames,filenames in os.walk(root):
    # skip .git and .venv and .tmp archive
    if '.git' in dirpath or '.venv' in dirpath or '.tmp' in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(('.py','.pyx','.cfg','.toml','.json','.yaml','.yml','.ini')):
            continue
        fp = os.path.join(dirpath,fn)
        try:
            with open(fp,'r',encoding='utf-8',errors='ignore') as f:
                data = f.read()
        except Exception:
            continue
        if '.agent_cache' in data or "'.agent_cache'" in data or '".agent_cache"' in data or "'.agent_cache/" in data:
            matches.append((fp, [m.start() for m in re.finditer(re.escape('.agent_cache'), data)]))
print('FOUND', len(matches), 'files')
for fp,pos in matches[:200]:
    print(fp)
# write to file
os.makedirs('.tmp', exist_ok=True)
with open('.tmp/agent_cache_refs.txt','w',encoding='utf-8') as out:
    for fp,pos in matches:
        out.write(fp+'\n')
print('\nWrote .tmp/agent_cache_refs.txt')
