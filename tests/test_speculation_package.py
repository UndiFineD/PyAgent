def test_speculation_package_import():
    import speculation  # noqa: F401
    assert hasattr(speculation, "__name__")
