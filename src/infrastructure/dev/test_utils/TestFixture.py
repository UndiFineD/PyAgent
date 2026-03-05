class TestFixture:
    """TestFixture shim for pytest collection."""

    def __init__(self, name: str = "fixture"):
        """Represents a test fixture for comparison."""
        self.name = name


__all__ = ["TestFixture"]
