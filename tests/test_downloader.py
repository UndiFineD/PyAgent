def test_download_repo(tmp_path):
    from importer import downloader

    target = tmp_path / "foo" / "bar"
    downloader.download_repo("foo/bar", target)
    assert target.exists()
    assert (target / "README.md").exists()
