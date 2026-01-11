#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""Central orchestrator for coordinating specialized AI agents in code improvement workflows."""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

    from src.logic.agents.swarm.OrchestratorAgent import *

if __name__ == '__main__':
    main()
