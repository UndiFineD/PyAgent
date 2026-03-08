#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

from auto_fix.rule_engine import RuleEngine


def test_basic_fixes_dedent_imports(tmp_path):
    """Test that the basic_fixes rule correctly dedents imports that are indented but not actually part of a block."""
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
    """Test that the basic_fixes rule correctly wraps an unguarded main() call in a guard."""
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


def test_indent_after_control_with_comments():
    """Imports following a control-statement should be indented even if a
    comment intervenes.
    """
    content = (
        "try:\n"
        "    pass\n"
        "# comment\n"
        "import os\n"
    )
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("foo.py", content)
    assert len(fixes) == 1
    assert "    import os" in fixes[0].replacement


def test_indent_after_type_checking():
    """Lines immediately after ``if TYPE_CHECKING:`` should be indented.

    Both imports and simple assignments (aliases) are common in these blocks.
    """
    content = (
        "if TYPE_CHECKING:\n"
        "from typing import List\n"
        "Alias = int\n"
        "# comment\n"
        "print('runtime')\n"
    )
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("typing_support.py", content)
    assert len(fixes) == 1
    replaced = fixes[0].replacement
    assert "    from typing import List" in replaced
    assert "    Alias = int" in replaced
    # the runtime print should not be indented since it belongs outside
    assert "print('runtime')" in replaced


def test_indent_after_header():
    """Statements immediately following a header must be indented.

    This covers ``def``/``class`` and control structures.  The fix only
    touches the first real line after the header and ignores blank lines or
    comments.
    """
    content = (
        "def foo():\n"
        "import hashlib\n"
        "# comment\n"
        "return 5\n"
        "\n"
        "if bar:\n"
        "print('oops')\n"
    )
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("header.py", content)
    assert len(fixes) == 1
    replaced = fixes[0].replacement
    assert "    import hashlib" in replaced
    assert "    print('oops')" in replaced
    # the comment following foo() should stay at top indentation
    assert "# comment" in replaced


def test_no_unnecessary_changes():
    """Test that the basic_fixes rule does not produce any fixes if the content is already clean."""
    content = "print('nothing to fix')\n"
    engine = RuleEngine.load_from_dir("src/auto_fix/rules")
    fixes = engine.evaluate("x.py", content)
    assert fixes == []
