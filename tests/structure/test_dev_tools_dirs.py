
from pathlib import Path

def test_dev_tools_structure(tmp_path: Path) -> None:
    """`src/tools` and `docs/` should be created by the setup helper."""
    from scripts.setup_structure import create_core_structure

    create_core_structure(str(tmp_path))
    # verify development‑tools locations
    assert (tmp_path / "src" / "tools").exists()
    assert (tmp_path / "docs").exists()
