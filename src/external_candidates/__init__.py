import sys
from pathlib import Path

# Ensure `src` is on sys.path so code that expects a src layout can still import.
ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

