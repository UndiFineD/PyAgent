def test_roadmap_cli(tmp_path):
    from roadmap import cli

    outdir = tmp_path / "output"
    outdir.mkdir()
    cli.generate(outdir)
    files = list(outdir.iterdir())
    assert files, "No file produced by CLI"
