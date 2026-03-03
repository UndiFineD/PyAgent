#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

from auto_fix.rule_engine import RuleEngine


def test_basic_fixes_dedent_imports(tmp_path):
    # simulate a file with a stray indented import in the middle of top-level
    content = (
        "from os import path\n"
        "    from sys import argv\n"
        "print('hello')\n"
    )
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate(str(tmp_path / "dummy.py"), content)
    assert len(fixes) == 1
    fixed = fixes[0].replacement
    assert "from sys import argv\n" in fixed
    assert not fixed.splitlines()[1].startswith(" ")


def test_basic_fixes_wrap_main():
    content = (
        "def main():\n"
        "    print('ok')\n"
        "\n"
        "main()\n"
    )
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("somefile.py", content)
    assert len(fixes) == 1
    replacement = fixes[0].replacement
    assert "if __name__ == '__main__':" in replacement
    assert "    main()" in replacement


def test_no_unnecessary_changes():
    content = "print('nothing to fix')\n"
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("x.py", content)
    assert fixes == []
