#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
from src.classes.strategies import *

# Type alias for functional compatibility
BackendFunction = Callable[
    [str, 
     Optional[str], 
     Optional[List[Dict[str, str]]]], 
    str]
