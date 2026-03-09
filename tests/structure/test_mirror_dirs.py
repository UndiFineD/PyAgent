

def test_mirror_dirs_initial(tmp_path):
    """The mirror directories should not exist after initial setup."""
    assert not (tmp_path / "tests" / "core").exists()
    assert not (tmp_path / "tests" / "agents").exists()
