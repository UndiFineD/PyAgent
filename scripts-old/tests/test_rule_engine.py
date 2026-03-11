#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");



from auto_fix.rule_engine import Fix, RuleEngine


def test_evaluate_simple_rule():
    """Test that a simple rule can be evaluated correctly
    """
    class DummyRule:
        """a simple rule that replaces 'foo' with 'bar'"""

        def check(self, content: str):
            """Returns a fix if 'foo' is in the content"""
            if "foo" in content:
                return [Fix(path="x", original=content, replacement=content.replace("foo", "bar"), description="swap")]
            return []

    engine = RuleEngine([DummyRule()])
    fixes = engine.evaluate("any", "foo baz")
    assert len(fixes) == 1
    assert fixes[0].replacement == "bar baz"


def test_load_from_dir(tmp_path):
    """Test that rules can be loaded from a directory"""
    # create a valid rule file
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    rule_code = (
        "def check(content: str):\n"
        "    if 'hello' in content:\n"
        "        return [{'path': 'a','original': content,'replacement': content.replace('hello','world'),'description':'r'}]\n"
        "    return []\n"
    )
    (rules_dir / "r1.py").write_text(rule_code, encoding="utf-8")

    engine = RuleEngine.load_from_dir(str(rules_dir))
    fixes = engine.evaluate("a.py", "hello")
    assert len(fixes) == 1
    assert fixes[0].replacement == "world"

    # loading from non-existent directory should yield no rules
    engine2 = RuleEngine.load_from_dir(str(tmp_path / "nope"))
    assert engine2.rules == []

    # broken rule should be ignored
    (rules_dir / "bad.py").write_text("raise RuntimeError()", encoding="utf-8")
    engine3 = RuleEngine.load_from_dir(str(rules_dir))
    # should still load the original valid rule
    fixes = engine3.evaluate("a.py", "hello")
    assert len(fixes) == 1
