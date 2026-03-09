def test_memory_package_import():
    import memory  # noqa: F401
    assert hasattr(memory, "__name__")
