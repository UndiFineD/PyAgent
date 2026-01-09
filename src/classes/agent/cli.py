#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from .Agent import Agent
from .HealthChecker import HealthChecker
from .RateLimitConfig import RateLimitConfig
from .utils import setup_logging

def _parse_quick_flag(val: str) -> dict:
    """format 'provider:model' or 'model'"""
    if not val:
        return {}
    if ':' in val:
        provider, model = val.split(':', 1)
        return {'provider': provider.strip(), 'model': model.strip()}
    return {'model': val.strip()}

def parse_model_overrides(raw_list: list[str] | None) -> dict[str, dict]:
    """Parse repeatable `--model` entries of form `agent=provider:model` or `agent=model`.

    Returns mapping agent -> spec dict.
    """
    out: dict[str, dict] = {}
    if not raw_list:
        return out
    for entry in raw_list:
        try:
            if '=' not in entry:
                logging.warning(f"Ignoring malformed --model entry: {entry}")
                continue
            agent_key, spec = entry.split('=', 1)
            agent_key = agent_key.strip()
            if ':' in spec:
                provider, model = spec.split(':', 1)
                out[agent_key] = {'provider': provider.strip(), 'model': model.strip()}
            else:
                out[agent_key] = {'model': spec.strip()}
        except Exception:
            logging.warning(f"Failed to parse --model entry: {entry}")
    return out

def main() -> None:
    """CLI entry point for the Agent Orchestrator."""
    parser = argparse.ArgumentParser(
        description='Agent: Orchestrates code improvement agents'
    )
    parser.add_argument('--dir', default='.', help='Directory to process (default: .)')
    parser.add_argument('--agents-only', action='store_true',
                        help='Only process files in the scripts / agent directory')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--loop', type=int, default=1,
                        help='Number of times to loop through all files (default: 1)')
    parser.add_argument('--skip-code-update', action='store_true',
                        help='Skip code updates and tests, only update documentation')
    parser.add_argument('--verbose', default='normal',
                        help='Verbosity level: quiet, minimal, normal, elaborate (or 0-3)')
    parser.add_argument('--no-git', action='store_true',
                        help='Skip git commit and push operations')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files')
    parser.add_argument(
        '--only-agents',
        type=str,
        metavar='AGENTS',
        help='Comma-separated list of agents to execute (e.g., coder,tests,documentation)')
    parser.add_argument('--timeout', type=int, metavar='SECONDS', default=120,
                        help='Default timeout per agent in seconds (default: 120)')
    parser.add_argument('--strategy', choices=['direct', 'cot', 'reflexion'], default='direct',
                        help='Reasoning strategy to use (direct, cot, reflexion)')
    # Phase 4c: Parallel execution arguments
    parser.add_argument('--async', dest='enable_async', action='store_true',
                        help='Enable async file processing for concurrent I / O')
    parser.add_argument('--multiprocessing', dest='enable_multiprocessing', action='store_true',
                        help='Enable multiprocessing for parallel agent execution')
    parser.add_argument('--workers', type=int, default=4,
                        help='Number of worker threads / processes (default: 4)')
    parser.add_argument('--webhook', type=str, action='append',
                        help='Register webhook URL for notifications (can be used multiple times)')
    # Phase 6: New feature arguments
    parser.add_argument('--config', type=str, metavar='FILE',
                        help='Path to configuration file (YAML / TOML / JSON)')
    parser.add_argument('--agent-models', type=str,
                        help='JSON string mapping agent->model spec (e.g. "{"coder": {"provider": "google", "model": "gemini-3"}}")')
    parser.add_argument('--model-coder', type=str,
                        help='Quick override for coder model. Format: "provider:model" or just "model"')
    parser.add_argument('--model-improvements', type=str,
                        help='Quick override for improvements model. Format: "provider:model" or just "model"')
    parser.add_argument('--n8n', type=str, metavar='URL',
                        help='Register an n8n webhook URL to receive agent notifications')
    parser.add_argument('--model', action='append', metavar='AGENT=SPEC',
                        help='Repeatable. Specify per-agent model overrides. Format: agent=provider:model or agent=model')
    parser.add_argument('--rate-limit', type=float, metavar='RPS',
                        help='Rate limit API calls to RPS requests per second')
    parser.add_argument('--enable-file-locking', action='store_true',
                        help='Enable file locking to prevent concurrent modifications')
    parser.add_argument('--incremental', action='store_true',
                        help='Only process files changed since last run')
    parser.add_argument('--graceful-shutdown', action='store_true',
                        help='Enable graceful shutdown with state persistence')
    parser.add_argument('--health-check', action='store_true',
                        help='Run health checks and exit')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous interrupted run')
    parser.add_argument('--diff-preview', action='store_true',
                        help='Show diffs before applying changes (requires --dry-run)')

    args = parser.parse_args()
    setup_logging(args.verbose)
    os.environ['DV_AGENT_VERBOSITY'] = args.verbose
    # Parse CLI model overrides
    cli_models: dict[str, dict] = {}
    if getattr(args, 'agent_models', None):
        try:
            import json as _json
            raw = _json.loads(args.agent_models)
            if isinstance(raw, dict):
                cli_models.update(raw)
        except Exception:
            logging.warning('Failed to parse --agent-models JSON; ignoring')

    if getattr(args, 'model_coder', None):
        cli_models.setdefault('coder', {}).update(_parse_quick_flag(args.model_coder))
    if getattr(args, 'model_improvements', None):
        cli_models.setdefault('improvements', {}).update(_parse_quick_flag(args.model_improvements))
    # Parse repeatable --model flags
    if getattr(args, 'model', None):
        parsed = parse_model_overrides(args.model)
        cli_models.update(parsed)

    # Health check mode
    if args.health_check:
        checker = HealthChecker(Path(args.dir).resolve())
        checker.run_all_checks()
        checker.print_report()
        sys.exit(0 if checker.is_healthy() else 1)

    # Load from config file if provided
    if args.config:
        agent = Agent.from_config_file(Path(args.config))
    else:
        # Parse selective agents if provided
        selective_agents = None
        if args.only_agents:
            selective_agents = [a.strip() for a in args.only_agents.split(',')]
            logging.info(f"Running with selective agents: {selective_agents}")

        agent = Agent(
            repo_root=args.dir,
            agents_only=args.agents_only,
            max_files=args.max_files,
            loop=args.loop,
            skip_code_update=args.skip_code_update,
            no_git=args.no_git,
            dry_run=args.dry_run,
            selective_agents=selective_agents,
            timeout_per_agent={'coder': args.timeout, 'tests': args.timeout},
            enable_async=args.enable_async,
            enable_multiprocessing=args.enable_multiprocessing,
            max_workers=args.workers,
            strategy=args.strategy
        )

    # Merge CLI-provided model overrides into agent.models
    if hasattr(agent, 'models'):
        try:
            existing = getattr(agent, 'models', {}) or {}
            # CLI overrides win
            # Validate providers for simple known list
            allowed_providers = {'openai', 'google', 'anthropic'}
            def _validate_spec(spec: dict) -> bool:
                prov = spec.get('provider')
                if prov and prov not in allowed_providers:
                    logging.warning(f"Unknown provider '{prov}' in model spec; continuing")
                return True

            for k, v in cli_models.items():
                if isinstance(v, dict):
                    _validate_spec(v)

            merged = {**existing, **cli_models}
            agent.models = merged
        except Exception:
            logging.debug('Failed to merge CLI model overrides')

    # If n8n URL provided, register it as a webhook
    if getattr(args, 'n8n', None):
        agent.register_webhook(args.n8n)

    # Register webhooks if provided
    if args.webhook:
        for webhook_url in args.webhook:
            agent.register_webhook(webhook_url)

    # Enable rate limiting if provided
    if args.rate_limit:
        agent.enable_rate_limiting(RateLimitConfig(
            requests_per_second=args.rate_limit
        ))

    # Enable file locking if requested
    if args.enable_file_locking:
        agent.enable_file_locking()

    # Enable incremental processing if requested
    if args.incremental:
        agent.enable_incremental_processing()

    # Enable graceful shutdown if requested
    if args.graceful_shutdown:
        agent.enable_graceful_shutdown()

    # Enable diff preview if requested
    if args.diff_preview:
        agent.enable_diff_preview()

    # Resume from previous run if requested
    if args.resume:
        pending_files = agent.resume_from_shutdown()
        if pending_files:
            logging.info(f"Resuming with {len(pending_files)} pending files")

    try:
        agent.run()
    finally:
        # Always print metrics summary
        agent.print_metrics_summary()

        # Cleanup graceful shutdown state on successful completion
        if hasattr(agent, 'shutdown_handler'):
            agent.shutdown_handler.cleanup()

        # Save incremental processing state
        if hasattr(agent, 'incremental_processor'):
            agent.incremental_processor.complete_run()

