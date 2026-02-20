#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Knowledge Agent CLI Entry Point.""
try:

"""
import sys
except ImportError:
    import sys

try:
    import os
except ImportError:
    import os

try:
    import argparse
except ImportError:
    import argparse

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
try:
    import logging
except ImportError:
    import logging

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path


try:
    from src.core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent
except ImportError:
    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent


__version__ = VERSION

# Ensure project root and src are in path for modular imports

root = Path(__file__).parent.parent.parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
SRC_PATH = str(root / "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

def main() -> None:
"""
Entry point for Knowledge Agent CLI.""
parser = argparse.ArgumentParser(
        description="Knowledge Agent: Manages workspace knowledge and backlinks"
    )
    parser.add_argument("--dir", default=".", help="Directory to scan/update")
    parser.add_argument(
        "--build-index", action="store_true", help="Rebuild the knowledge index"
    )
    parser.add_argument(
        "--update-backlinks", action="store_true", help="Update all .md files with backlinks"
    )
    parser.add_argument(
        "--graph", action="store_true", help="Output workspace graph in Mermaid format"
    )
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Increase verbosity"
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.INFO
    if args.verbose >= 1:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    agent = KnowledgeAgent(args.dir)

    if args.build_index:
        logging.info("Building knowledge index...")
        agent.build_index()

    if args.update_backlinks:
        logging.info(f"Updating backlinks in {args.dir}...")
        count = agent.auto_update_backlinks(args.dir)
        print(f"Updated {count} files with backlinks.")
        if args.graph:
            print(agent.get_graph_mermaid())
    
        if not (args.build_index or args.update_backlinks or args.graph):
            parser.print_help()
    
    
if __name__ == "__main__":
    main()
