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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



# -*- coding: utf-8 -*-

"""Utility classes for BaseAgent framework."""


import hashlib
import json
import logging
import argparse
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .agent import BaseAgent

try:
    from src.logic.strategies import plan_executor as agent_strategies
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from src.logic.strategies import plan_executor as agent_strategies
from .models import AgentEvent, FilePriority, InputType, AgentState, ResponseQuality


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on verbosity level."""
    level = logging.INFO
    if verbosity_arg >= 2:
        level = logging.DEBUG
    elif verbosity_arg == 1:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )


def as_tool(priority: int = 0, category: Optional[str] = None) -> Callable:
    """Decorator to mark a method as a tool for the ToolRegistry.
    Automatically records tool interactions to the fleet context shards for autonomous learning.
    Can be used as @as_tool or @as_tool(priority=10).
    """
    from functools import wraps
    import time

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            # Phase 108: Enhanced Traceability
            logging.debug(f"Executing tool {func.__name__} on {self.__class__.__name__}")
            
            result = func(self, *args, **kwargs)
            
            # Autonomous Logic Harvesting:
            if hasattr(self, "fleet") and self.fleet and hasattr(self.fleet, "recorder"):
                try:
                    shard_result = str(result)
                    if len(shard_result) > 2000:
                        shard_result = shard_result[:2000] + "... [TRUNCATED]"
                    
                    prompt_trace = f"TOOL_EXECUTION: {func.__name__}\nArgs: {args}\nKwargs: {kwargs}"
                    
                    self.fleet.recorder.record_interaction(
                        provider="agent_tool",
                        model=self.__class__.__name__,
                        prompt=prompt_trace,
                        result=shard_result,
                        meta={
                            "tool": func.__name__,
                            "agent": self.__class__.__name__,
                            "timestamp_ms": int(time.time() * 1000)
                        }
                    )
                except Exception as e:
                    logging.debug(f"Failed to record tool interaction: {e}")
                    
            return result

        wrapper._is_tool = True
        wrapper._tool_priority = priority
        if category:
            wrapper._tool_category = category
        return wrapper

    # Support @as_tool without parentheses
    if callable(priority):
        f = priority
        priority = 0
        return decorator(f)
        
    return decorator

def create_main_function(
    agent_class: Type[BaseAgent],
    description: str,
    context_help: str) -> Callable[[],
                                   None]:
    """Create a main function for an agent class."""
    def main() -> None:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '--describe-backends',
            action='store_true',
            help='Print which AI backends are available / configured and exit',
        )
        parser.add_argument(
            '--backend',
            choices=['auto', 'copilot', 'gh', 'github-models'],
            default=None,
            help='Select backend (overrides DV_AGENT_BACKEND for this run only)',
        )
        parser.add_argument(
            '--strategy',
            choices=['direct', 'cot', 'reflexion'],
            default='direct',
            help='Select reasoning strategy (direct, cot, reflexion)',
        )
        parser.add_argument(
            '--verbose',
            '-v',
            action='count',
            default=0,
            help='Increase verbosity (can be used multiple times, e.g. -vv)',
        )
        parser.add_argument(
            '--no-cascade',
            action='store_true',
            help='Prevent this agent from launching other agents (internal use)',
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output result as JSON (useful for n8n/automation integration)',
        )
        parser.add_argument('--context', required=True, help=context_help)
        parser.add_argument('--prompt', required=True, help='Prompt for improving the content')
        parser.add_argument('--delegate', help='Agent type to delegate a sub-task to (e.g., SearchAgent)')
        args = parser.parse_args()
        setup_logging(args.verbose)
        
        if args.backend:
            os.environ['DV_AGENT_BACKEND'] = args.backend
            
        agent = agent_class(args.context)
        
        # If delegation is requested via CLI
        if args.delegate:
            logging.info(f"CLI Delegation: {agent_class.__name__} -> {args.delegate}")
            result = agent.delegate_to(args.delegate, args.prompt)
            if args.json:
                print(json.dumps({"delegation_result": result}))
            else:
                print(f"Delegation Result:\n{result}")
            return

        # Normal execution
        # Honor parent/guard flag to avoid cascading agent invocations
        if getattr(args, 'no_cascade', False) or os.environ.get('DV_AGENT_PARENT'):
            agent._no_cascade = True
            logging.info('No-cascade mode enabled for this agent (prevents spawning other agents)')

        # Set strategy based on argument
        if args.strategy == 'cot':
            agent.set_strategy(agent_strategies.ChainOfThoughtStrategy())
        elif args.strategy == 'reflexion':
            agent.set_strategy(agent_strategies.ReflexionStrategy())
        else:
            agent.set_strategy(agent_strategies.DirectStrategy())

        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()
        
        if args.json:
            result = {
                "agent": agent_class.__name__,
                "file_path": str(agent.file_path),
                "updated": bool(diff),
                "diff": diff,
                "content_length": len(agent.current_content)
            }
            print(json.dumps(result, indent=2))
        else:
            if diff:
                logging.info(f"{agent_class.__name__.replace('Agent', '').lower()} updated:")
                logging.info(diff)
            else:
                logging.info(f"No changes made to {agent_class.__name__.replace('Agent', '').lower()}.")
    return main
