from pathlib import Path
import subprocess

from typing import Any


def test_compile_diagrams(tmp_path: Path, monkeypatch: Any) -> None:
    """Test that the compile_diagrams script correctly 
    processes .mmd files into .svg files.
    """
    # copy a simple diagram to the temp architecture directory
    arch = tmp_path / "docs" / "architecture"
    arch.mkdir(parents=True)
    mmd = arch / "example.mmd"
    mmd.write_text("graph TD; A-->B")
    # monkeypatch the global path in script
    import scripts.compile_diagrams as cd
    cd.diagram_dir = arch

    # stub subprocess.run to create an output file instead of calling mmdc
    def fake_run(cmd: list[str], **kwargs: Any) -> None:
        """Fake subprocess.run that simulates mmdc by creating an SVG file."""
        # ignore check and other kwargs (kwargs is intentionally unused)
        out_index = cmd.index("-o") + 1
        Path(cmd[out_index]).write_text("svg", encoding="utf-8")

    monkeypatch.setattr(subprocess, "run", fake_run)
    cd.compile_diagrams()
    assert (arch / "example.svg").is_file()
