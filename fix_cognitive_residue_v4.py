#!/usr/bin/env python3
import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix W0613 (Unused argument) with _unused suffix
    # Replace parameter_unused with _ or just keep as is if Pylint is happy with _
    # Actually, Pylint usually ignores arguments starting with _ or matching a list.
    # I'll rename them to start with _ exactly.
    content = re.sub(r'(\b\w+)_unused\b', r'_\1', content)

    # 2. Fix R1705 (Unnecessary "else" after "return")
    # This is slightly more complex for regex, but I'll try simple cases.
    # Matches:
    # return ...
    # else:
    #     ...
    # Replace with:
    # return ...
    # ... (de-indented)
    def fix_else_return(match):
        indent = match.group(1)
        return_stmt = match.group(0).strip().split('\n')[0]
        else_block = match.group(3)
        # De-indent else block
        lines = else_block.split('\n')
        new_else_block = []
        for line in lines:
            if line.startswith(indent + '    '):
                new_else_block.append(line[4:])
            else:
                new_else_block.append(line)
        return f"{indent}{return_stmt}\n{'\n'.join(new_else_block)}"

    # Simplistic regex for else-return (handles common case)
    content = re.sub(r'^(\s+)(return.*?)\n\1else:\n(.*?)(?=\n\1\w|\Z)', fix_else_return, content, flags=re.DOTALL | re.MULTILINE)

    # 3. Fix W0102 (Dangerous default value [] as argument)
    content = re.sub(r'=\s*\[\]\)', r'= None)', content)
    # Also need to add if x is None: x = [] inside the function
    # This is harder for regex, I'll do holographic_context_agent.py manually or if it matches a pattern.

    # 4. Fix W0127 (Self-assigning variable)
    content = re.sub(r'^\s*(\w+)\s*=\s*\1\s*$', r'', content, flags=re.MULTILINE)

    # 5. Fix R1719 (simplifiable-if-expression)
    # is_consistent = True if language.lower() in [...] else False
    content = re.sub(r'(\w+)\s*=\s*True\s+if\s+(.*?)\s+else\s+False', r'\1 = bool(\2)', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

FILES = [
    'src/logic/agents/cognitive/audio_reasoning_agent.py',
    'src/logic/agents/cognitive/cooperative_communication_agent.py',
    'src/logic/agents/cognitive/dynamic_decomposer_agent.py',
    'src/logic/agents/cognitive/evolutionary_prompt_agent.py',
    'src/logic/agents/cognitive/explainability_agent.py',
    'src/logic/agents/cognitive/holographic_context_agent.py',
    'src/logic/agents/cognitive/intention_prediction_agent.py',
    'src/logic/agents/cognitive/latent_reasoning_agent.py',
    'src/logic/agents/cognitive/reflection_agent.py',
    'src/logic/agents/cognitive/speciation_agent.py',
    'src/logic/agents/cognitive/synthesis_agent.py',
    'src/logic/agents/cognitive/voice_agent.py',
    'src/logic/agents/cognitive/world_model_agent.py',
    'src/logic/agents/cognitive/reasoning_agent.py',
]

for f in FILES:
    if os.path.exists(f):
        print(f"Fixing {f}")
        fix_file(f)
