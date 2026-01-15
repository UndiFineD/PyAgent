"""Legacy unit tests for observability statistics."""
from pathlib import Path
try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass




def test_stats_agent_counts_files(tmp_path: Path) -> None:
    with agent_dir_on_path():
        from src.observability.stats.agents import StatsAgent

    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_text("print('a')\n", encoding="utf-8")
    b.write_text("print('b')\n", encoding="utf-8")
    # Only `a` has companions.
    (tmp_path / "a.description.md").write_text("desc", encoding="utf-8")
    (tmp_path / "a.changes.md").write_text("chg", encoding="utf-8")
    (tmp_path / "a.errors.md").write_text("err", encoding="utf-8")
    (tmp_path / "a.improvements.md").write_text("imp", encoding="utf-8")
    (tmp_path / "test_a.py").write_text("def test_a() -> None:\n    assert True\n", encoding="utf-8")
    agent = StatsAgent([str(a), str(b)])
    stats = agent.calculate_stats()
    assert stats["total_files"] == 2
    assert stats["files_with_context"] == 1
    assert stats["files_with_changes"] == 1
    assert stats["files_with_errors"] == 1
    assert stats["files_with_improvements"] == 1
    assert stats["files_with_tests"] == 1
