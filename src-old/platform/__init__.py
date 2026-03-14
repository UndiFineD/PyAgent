r"""Safe platform shim that delegates to the stdlib's platform.py when available.
Avoids recursion by loading the stdlib implementation directly from the stdlib path.
If the stdlib platform module is not found, provides a minimal fallback for tests.
"""
