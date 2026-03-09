

def test_cov_option_present() -> None:
    """pytest.ini should contain the --cov option for coverage reporting."""
    # read pytest.ini to ensure coverage addopts configured
    content = open("pytest.ini").read()
    assert "--cov=src" in content
