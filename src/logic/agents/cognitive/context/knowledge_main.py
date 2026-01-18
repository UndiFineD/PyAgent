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
Knowledge Agent: Manages workspace knowledge and backlinks.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import sys
import argparse
import logging
from pathlib import Path

__version__ = VERSION

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

    from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent

def main() -> None:
    parser = argparse.ArgumentParser(description='Knowledge Agent: Manages workspace knowledge and backlinks')
    parser.add_argument('--dir', default='.', help='Directory to scan/update')
    parser.add_argument('--build-index', action='store_true', help='Rebuild the knowledge index')
    parser.add_argument('--update-backlinks', action='store_true', help='Update all .md files with backlinks')
    parser.add_argument('--graph', action='store_true', help='Output workspace graph in Mermaid format')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase verbosity')
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.INFO
    if args.verbose >= 1:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    
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

if __name__ == '__main__':
    main()