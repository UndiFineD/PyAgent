#!/usr/bin/env python3
"""Test the roadmap CLI."""

from pathlib import Path

from src.roadmap import cli, vision


def test_roadmap_cli(tmp_path: Path) -> None:
    """Test the roadmap CLI."""
    outdir = tmp_path / "output"
    outdir.mkdir()
    cli.generate(outdir)
    files = list(outdir.iterdir())
    assert files, "No file produced by CLI"


def test_roadmap_cli_main_generate(tmp_path: Path) -> None:
    """main() generate subcommand writes a roadmap.md file."""
    outdir = tmp_path / "gen-out"
    rc = cli.main(["generate", "--out", str(outdir)])
    assert rc == 0
    assert (outdir / "roadmap.md").exists()


def test_roadmap_cli_main_vision(capsys) -> None:
    """main() vision subcommand prints the vision template."""
    rc = cli.main(["vision"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Vision" in out


def test_roadmap_cli_main_milestones(tmp_path: Path) -> None:
    """main() milestones subcommand writes a milestones file."""
    out_file = tmp_path / "ms.md"
    rc = cli.main(["milestones", "--out", str(out_file), "Phase 1", "Phase 2"])
    assert rc == 0
    content = out_file.read_text()
    assert "Phase 1" in content
    assert "Phase 2" in content


def test_vision_template_contains_pyagent() -> None:
    """Vision template should mention PyAgent and core principles."""
    template = vision.get_template()
    assert "PyAgent" in template
    assert "Vision" in template
