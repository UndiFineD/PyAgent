def test_transport_package_import():
    # package does not exist yet
    import transport  # noqa: F401
    assert hasattr(transport, "__name__")
