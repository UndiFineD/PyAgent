def test_multimodal_package_import():
    import multimodal  # noqa: F401
    assert hasattr(multimodal, "__name__")
