

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    version_lines = []
    others = []
    for line in lines:
        if 'from src.core.base.version import VERSION' in line or '__version__ = VERSION' in line:
            version_lines.append(line)
        else:
            others.append(line)

    if len(version_lines) == 2:
        # Find insertion point
        insert_pos = 0
        for i, line in enumerate(others):
            if line.startswith('import ') or line.startswith('from '):
                insert_pos = i
                break

        # If no imports found, insert after docstring or future
        if insert_pos == 0:
            for i, line in enumerate(others):
                if line.startswith('from __future__'):
                    insert_pos = i + 1
                    break

        final_lines = others[:insert_pos] + version_lines + others[insert_pos:]
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return True
    return False

# Files identified from ruff output


















files_to_fix = [
    'src/infrastructure/backend/LLMClient.py',
    'src/infrastructure/fleet/AgentEconomy.py',
    'src/infrastructure/fleet/AgentStore.py',
]

for f in files_to_fix:
    if fix_file(f):
        print(f"Fixed {f}")
