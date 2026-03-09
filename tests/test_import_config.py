import tempfile


def test_parse_manifest(tmp_path):
    from importer import config

    manifest = tmp_path / "github.md"
    manifest.write_text("foo/bar\n")

    repos = config.parse_manifest(manifest)
    assert repos == [("foo", "bar")]
