# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\test_import.py
#!/usr/bin/env python3
import sys

sys.path.insert(0, "src/praisonai-agents")

import warnings

warnings.simplefilter("always")

print("Testing import with warnings enabled...")
import praisonaiagents

print("Import successful!")
