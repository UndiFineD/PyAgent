#!/usr/bin/env python3
import os

root = os.path.join(os.getcwd(), 'src')
changed = []
for dirpath, _, files in os.walk(root):
    for f in files:
        if not f.endswith('_test.py'):
            continue
        path = os.path.join(dirpath, f)
        with open(path, 'r', encoding='utf-8') as fh:
            src = fh.read()
        new = src
        # Fix patterns: try:\nfrom src.
        new = new.replace('\ntry:\nfrom src.', '\ntry:\n    from src.')
        new = new.replace('\ntry:\nimport src.', '\ntry:\n    import src.')
        if new != src:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            changed.append(path)

print('fixed_files:', len(changed))
for p in changed:
    print('  ', p)
