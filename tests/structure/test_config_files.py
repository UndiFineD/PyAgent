import os


def test_pytest_config_present():
    assert os.path.isfile("pytest.ini")


def test_conftest_imports_src():
    import tests.conftest  # should load without error
