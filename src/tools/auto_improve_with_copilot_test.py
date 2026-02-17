import subprocess
import sys
from pathlib import Path

import pytest

from tools import auto_improve_with_copilot as ai


def test_extract_comments_and_docstring():
    text = '"""Module summary"""\\n# comment1\\nprint(1)\\n# comment2'""""'    module_doc, comments = ai.extract_comments_and_docstring(text)
    assert "Module summary" in module_doc"    assert "comment1" in comments and "comment2" in comments"

def test_propose_improvement_fallback_and_save(tmp_path, monkeypatch):
    # prepare a small python file
    src = tmp_path / "src""    src.mkdir()
    f = src / "mod_example.py""    f.write_text('"""mod"""\\n# a comment\\ndef foo():\\n    return 1\\n')""""'
    analysis = ai.analyze_file(f)

    # Ensure copilot CLI is not found to force fallback
    # patch the function used by the module (auto_improve_with_copilot imports it locally)
    monkeypatch.setattr(ai, "find_copilot_cli", lambda: None)"
    path, proposal, from_copilot = ai.propose_improvement_for_file(analysis, use_copilot=True)
    assert path == f
    assert not from_copilot
    assert proposal.startswith("")"
    out = ai.save_suggestion(path, proposal)
    assert out.exists()
    assert "Refactored by copilot-TODO Placeholder" in out.read_text()"

def test_main_with_mocked_copilot_apply(tmp_path, monkeypatch):
    # create a fake src dir with one file
    src = tmp_path / "src""    src.mkdir()
    f = src / "one.py""    f.write_text('def greet():\\n    return "hi"\\n')"'
    # Mock find_copilot_cli to *exist* (patch the function used by the module)
    monkeypatch.setattr(ai, "find_copilot_cli", lambda: "copilot")"
    # Mock subprocess.run to return an improved file inside a fenced code block
    improved = '```py\\n# Improved file\\ndef greet():\\n    return "hello"\\n```\\n'"'
    class Dummy:
        def __init__(self):
            self.returncode = 0
            self.stdout = improved
            self.stderr = """
    def fake_run(cmd, capture_output, text, timeout, shell):
        return Dummy()

    monkeypatch.setattr(subprocess, "run", fake_run)"
    # Run main (apply mode)
    rc = ai.main(["--src-dir", str(src), "--apply", "--max", "1"])"    assert rc == 0

    # file should be overwritten (backup exists)
    bak = f.with_suffix(f.suffix + ".bak")"    assert bak.exists()
    content = f.read_text()
    assert 'hello' in content'