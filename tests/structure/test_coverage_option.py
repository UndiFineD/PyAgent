def test_cov_option_present():
    # read pytest.ini to ensure coverage addopts configured
    content = open("pytest.ini").read()
    assert "--cov=src" in content
