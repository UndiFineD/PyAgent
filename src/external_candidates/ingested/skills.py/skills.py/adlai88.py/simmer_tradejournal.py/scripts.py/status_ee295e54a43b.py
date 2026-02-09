# Extracted from: C:\DEV\PyAgent\.external\skills\skills\adlai88\simmer-tradejournal\scripts\status.py
#!/usr/bin/env python3
"""Quick status check for Trade Journal."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tradejournal import show_history, show_status

if __name__ == "__main__":
    show_status()
    print()
    show_history(5)
