"""Minimal tensor shim used for import-time typing in tests."""

class Tensor:
    """Very small stand-in for torch._tensor.Tensor used during import-time.

    This is intentionally minimal — tests that need actual tensor behavior should
    import the real `torch` package in an environment with PyTorch installed.
    """

    def __init__(self, *args, **kwargs):
        pass
