import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from auto_fix.rule_engine import RuleEngine

engine = RuleEngine.load_from_dir('src/auto_fix/rules')
print('num rules', len(engine.rules))
for r in engine.rules:
    print('rule', r)
    try:
        print('test run', r.check('from os import path\n    from sys import argv\n'))
    except Exception as ex:
        print('rule execution failed', ex)
