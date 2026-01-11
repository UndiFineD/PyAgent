"""Script for final namespace correction and import migration."""

import os
import re

def fix_imports(content: str) -> str:
    """Migrate legacy module names to the src namespace."""
    modules = [
        'agent_backend', 'agent_changes', 'agent_coder', 'agent_context', 
        'agent_errors', 'agent_improvements', 'agent_knowledge', 'agent_search', 
        'agent_stats', 'agent_strategies', 'agent_tests', 'agent_test_utils'
    ]
    
    for mod in modules:
        content = re.sub(rf'^\s*from ({mod})(\b\s+import|\b\s+)', r'from src.\1\2', content, flags=re.MULTILINE)
        content = re.sub(rf'^\s*import ({mod})(\b\s*$)', r'from src import \1', content, flags=re.MULTILINE)

    content = content.replace('from classes.', 'from src.')
    # Fix src.agent -> src.logic.agents
    content = content.replace('from src.agent.', 'from src.logic.agents.')
    content = content.replace('import src.agent.', 'import src.logic.agents.')
    # Handle the specific case in agent_deprecated.py
    content = content.replace('from src.agent import *', 'from src.logic.agents.swarm.OrchestratorAgent import *') # Assuming Agent.py has the stuff
    
    return content

updated_count = 0
for root_dir in ['src', 'tests']:
    for root, dirs, files in os.walk(root_dir):
        if '__pycache__' in root or '.git' in root: continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = fix_imports(content)
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        updated_count += 1
                except: pass

print(f"Updated {updated_count} files.")
