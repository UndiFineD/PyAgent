def test_importer_flow(tmp_path):
    # end-to-end smoke using stubs
    from importer.config import parse_manifest
    from importer.downloader import download_repo
    from importer.describe import describe_file
    from importer.compile import compile_architecture

    manifest = tmp_path / "github.md"
    manifest.write_text("a/b\n")

    repos = parse_manifest(manifest)
    assert repos == [("a", "b")]

    target = tmp_path / "a" / "b"
    download_repo("a/b", target)

    info = describe_file(target / "README.md")
    assert info["size"] == 0

    out = tmp_path / "architecture.md"
    compile_architecture([info], out)
    assert out.exists()
    assert "README.md" in out.read_text()
