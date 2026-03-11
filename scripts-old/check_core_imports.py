import sys
from pathlib import Path


def run_check(module_path_parts, star_name):
    # Mimic test's sys.path manipulation
    src_path = Path('src')
    core_path = Path('src')
    # Insert src into sys.path
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Also mimic some tests inserting src/logic/agents/intelligence
    intelligence_path = Path('src/logic/agents/intelligence')
    if str(intelligence_path) not in sys.path:
        sys.path.insert(0, str(intelligence_path))

    print('sys.path[0]=', sys.path[0])
    try:
        mod_spec = '.'.join(module_path_parts)
        print('Importing', mod_spec)
        # perform star import into a fresh namespace dict
        ns = {}
        exec(f"from {mod_spec} import *", ns)
        exported = [k for k in ns.keys() if not k.startswith('_')]
        print('exported names:', exported)
        print(f"contains {star_name}?", star_name in exported)
    except Exception as e:
        print('Import failed:', type(e).__name__, e)

if __name__ == '__main__':
    checks = [
        (['logic','agents','intelligence','core','LocalizationCore'], 'LocalizationCore'),
        (['logic','agents','intelligence','core','SearchMeshCore'], 'SearchMeshCore'),
        (['logic','agents','intelligence','core','SynthesisCore'], 'SynthesisCore'),
    ]
    for parts, name in checks:
        run_check(parts, name)
        print('-' * 40)
