import sys

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'src'))
from auto_fix.rule_engine import RuleEngine


def main():
    engine = RuleEngine.load_from_dir('src/auto_fix/rules')
    content = "from os import path\n    from sys import argv\nprint('hi')\n"
    fixes = engine.evaluate('dummy.py', content)
    print('count', len(fixes))
    if fixes:
        print('replacement:')
        print(fixes[0].replacement)

if __name__ == '__main__':
    main()
