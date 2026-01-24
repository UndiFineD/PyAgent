#!/usr/bin/env python3
import os
import re

files = [
    "knowledge_fusion_agent.py",
    "latent_reasoning_agent.py",
    "linguistic_agent.py",
    "memory_consolidation_agent.py",
    "neuro_symbolic_agent.py",
    "proactive_agent.py",
    "reality_grafting_agent.py",
    "reasoning_agent.py",
    "reflection_agent.py",
    "visualizer_agent.py",
    "voice_agent.py"
]

root = "src/logic/agents/cognitive"

for filename in files:
    path = os.path.join(root, filename)
    if not os.path.exists(path):
        print(f"Skipping {path} (not found)")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Fix non-async improve_content
    pattern = r'def improve_content\(self, prompt: str\)\s*->\s*str:'
    replacement = 'async def improve_content(self, prompt: str, target_file: str | None = None) -> str:'
    
    new_content = re.sub(pattern, replacement, content)
    
    # 2. Add docstrings and unused markers if missing
    # We look for the newly replaced async def and check the next few lines
    lines = new_content.splitlines()
    for i, line in enumerate(lines):
        if 'async def improve_content(self, prompt: str, target_file: str | None = None) -> str:' in line:
            # Check if body already has the markers
            found_marker = False
            for j in range(i+1, min(i+5, len(lines))):
                if '_ = target_file' in lines[j]:
                    found_marker = True
                    break
            
            if not found_marker:
                # Insert at i+1
                indent = re.match(r'^\s*', line).group()
                new_indent = indent + "    "
                docstring = f'{new_indent}"""Optimizes fleet content based on cognitive reasoning."""'
                marker1 = f'{new_indent}_ = prompt'
                marker2 = f'{new_indent}_ = target_file'
                
                # If the next line is a return or a call, insert these
                if i+1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line.startswith("return") or not next_line:
                        lines.insert(i+1, marker2)
                        lines.insert(i+1, marker1)
                        lines.insert(i+1, docstring)
    
    final_content = "\n".join(lines)
    
    if final_content != content:
        print(f"Update signatures in {path}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
    else:
        print(f"No changes needed for {path}")
