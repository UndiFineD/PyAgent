#!/usr/bin/env python3
import os
import re

def fix_improve_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match sync improve_content(self, prompt)
    # def improve_content(self, prompt: str) -> str:
    pattern = r'def improve_content\(self, prompt: str\) -> str:'
    replacement = 'async def improve_content(self, prompt: str, target_file: str | None = None) -> str:\n        _ = target_file'
    
    if re.search(pattern, content):
        print(f"Standardizing improve_content in {filepath}")
        content = re.sub(pattern, replacement, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

base_dir = r"c:\DEV\PyAgent\src\logic\agents\cognitive"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py'):
            fix_improve_content(os.path.join(root, file))
