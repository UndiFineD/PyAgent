# Extracted from: C:\DEV\PyAgent\.external\skills\skills\officialpm\my-tesla\tests\__init__.py
"""Test package for my-tesla.

We explicitly disable bytecode writing so running tests doesn't create __pycache__
folders inside the repo (keeps the private repo clean + avoids accidental noisy
artifacts).
"""

import sys

sys.dont_write_bytecode = True
