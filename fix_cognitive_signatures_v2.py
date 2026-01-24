#!/usr/bin/env python3
import os
import re

root = "src/logic/agents/cognitive"
for filename in os.listdir(root):
    if not filename.endswith(".py"): continue
    path = os.path.join(root, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        continue
    
    # Target all variations of improve_content
    # Handles:
    # def improve_content(self, prompt: str) -> str:
    # async def improve_content(self, prompt: str) -> str:
    # def improve_content(self, content: str) -> str:
    # etc.
    
    # Simplified regex that just looks for the name and parameters until the closing paren
    pattern = r'(async\s+)?def improve_content\s*\(\s*self\s*,\s*[^)]*?\)\s*->\s*str\s*:'
    
    replacement = 'async def improve_content(self, prompt: str, target_file: str | None = None) -> str:'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        print(f"Fixed signature in {filename}")
        lines = new_content.splitlines()
        # Find the line we just changed
        for i, line in enumerate(lines):
            if replacement in line:
                indent = re.match(r'^\s*', line).group()
                new_indent = indent + "    "
                
                # Check next line for docstring/markers
                # (We skip the lines that were part of the old method body if they survived)
                # To be safe, we just insert and let the user (or Pylint) handle redundancy if any,
                # but we'll try to check.
                
                found_docstring = False
                found_markers = False
                
                # Peek ahead 5 lines
                for j in range(i+1, min(i+10, len(lines))):
                    l_strip = lines[j].strip()
                    if l_strip.startswith('"""') or l_strip.startswith("'''"):
                        found_docstring = True
                    if '_ = target_file' in l_strip:
                        found_markers = True
                
                if not found_markers:
                    lines.insert(i+1, f'{new_indent}_ = target_file')
                    lines.insert(i+1, f'{new_indent}_ = prompt')
                
                if not found_docstring:
                    lines.insert(i+1, f'{new_indent}"""Optimizes fleet content based on cognitive reasoning."""')
                
                break # Only one per file
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
