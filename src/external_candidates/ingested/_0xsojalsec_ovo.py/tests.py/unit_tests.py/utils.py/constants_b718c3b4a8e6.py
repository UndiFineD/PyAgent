# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\utils\constants.py
import os
from enum import Enum

TIMEOUT = 15
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OVO_PAGES = os.path.join(REPO_ROOT, "ovo", "app", "pages")

JOBS_FILE = os.path.join(OVO_PAGES, "jobs", "jobs.py")
SCAFFOLD_DESIGN_FILE = os.path.join(OVO_PAGES, "rfdiffusion", "scaffold_design.py")
BINDER_DESIGN_FILE = os.path.join(OVO_PAGES, "rfdiffusion", "binder_design.py")
EXPORT_FILE = os.path.join(OVO_PAGES, "export.py")
DESIGNS_FILE = os.path.join(OVO_PAGES, "designs", "designs.py")
