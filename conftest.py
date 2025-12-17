"""Pytest configuration for PyAgent tests."""
import sys
from pathlib import Path

# Add the root directory to sys.path so that tests can import from tests package
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
