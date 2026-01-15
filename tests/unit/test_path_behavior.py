"""Test script to verify Path behavior with mock objects."""
from pathlib import Path




class MockFleet:
    """Mock fleet class for path testing."""
    pass



f = MockFleet()
try:
    p = Path(f)
    print(f"Path(f) is {p}")
    print(f"Type: {type(p)}")
except Exception as e:
    print(f"Error: {e}")
