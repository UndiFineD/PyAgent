#!/usr/bin/env python3
"""Test that the transport package can be imported and has expected attributes."""


def test_transport_package_import() -> None:
    """The transport package should be importable and have expected attributes."""
    # package should be importable and expose runtime validation hook.
    import transport  # noqa: F401

    assert hasattr(transport, "__name__")
    assert transport.validate() is True
