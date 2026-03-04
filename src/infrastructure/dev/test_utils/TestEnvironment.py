class TestEnvironment:
    """TestEnvironment shim for pytest collection."""
    def __init__(self, name: str = "default"):
        """Represents a test environment for comparison."""
        self.name = name

__all__ = ["TestEnvironment"]
