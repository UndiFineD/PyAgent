#!/usr/bin/env python3
import json
import sys
import os

def normalize(p):
    return p.replace('\\','/').lower()

if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: remove_lint_entries.py <file1> [file2 ...]')
        sys.exit(2)
    targets = {normalize(p) for p in sys.argv[1:]}
    path = os.path.join('temp','lint_results.json')
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    new = [e for e in data if normalize(e.get('file','')) not in targets]
    with open(path,'w',encoding='utf-8') as f:
        json.dump(new,f,indent=2)
    print('removed', len(data)-len(new), 'entries')
