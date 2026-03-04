class TestBaseline:
    """TestBaseline shim for pytest collection."""
    def __init__(self, name: str, data=None):
        """Represents a test baseline for comparison."""
        self.name = name
        self.data = data

__all__ = ["TestBaseline"]
