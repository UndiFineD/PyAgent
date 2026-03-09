def test_rl_package_import():
    import rl  # noqa: F401
    assert hasattr(rl, "__name__")
