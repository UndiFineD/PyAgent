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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.AgentConfig import AgentConfig
from src.core.base.models import AgentPluginConfig, ConfigFormat, RateLimitConfig
from pathlib import Path
from typing import Any, cast
import json
import logging

__version__ = VERSION







class ConfigLoader:
    """Loads agent configuration from YAML / TOML / JSON files.

    Supports multiple configuration file formats and provides
    validation and merging of configuration options.

    Attributes:
        config_path: Path to configuration file.
        format: Configuration file format.
    """

    SUPPORTED_EXTENSIONS = {
        '.yaml': ConfigFormat.YAML,
        '.yml': ConfigFormat.YAML,
        '.toml': ConfigFormat.TOML,
        '.json': ConfigFormat.JSON,
        '.ini': ConfigFormat.INI,
    }

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize the config loader.

        Args:
            config_path: Path to configuration file.
        """
        self.config_path = config_path
        self.format: ConfigFormat | None = None

        if config_path:
            ext = config_path.suffix.lower()
            self.format = self.SUPPORTED_EXTENSIONS.get(ext)

    def load(self) -> AgentConfig:
        """Load configuration from file.

        Returns:
            AgentConfig with loaded settings.
        """
        if not self.config_path or not self.config_path.exists():
            return AgentConfig()

        try:
            content = self.config_path.read_text()
            data = self._parse_content(content)
            return self._build_config(data)
        except Exception as e:
            logging.error(f"Failed to load config from {self.config_path}: {e}")
            return AgentConfig()

    def _parse_content(self, content: str) -> dict[str, Any]:
        """Parse configuration content based on format."""
        if self.format == ConfigFormat.JSON:
            raw: Any = json.loads(content)
            return cast(dict[str, Any], raw) if isinstance(raw, dict) else {}
        elif self.format == ConfigFormat.YAML:
            try:
                import yaml
                raw: Any = yaml.safe_load(content)
                return cast(dict[str, Any], raw) if isinstance(raw, dict) else {}
            except ImportError:
                logging.warning("PyYAML not installed, falling back to JSON")
                return {}
        elif self.format == ConfigFormat.TOML:
            try:
                import tomllib
                raw: Any = tomllib.loads(content)
                return cast(dict[str, Any], raw) if isinstance(raw, dict) else {}
            except ImportError:
                try:
                    import toml
                    raw: Any = toml.loads(content)
                    return cast(dict[str, Any], raw) if isinstance(raw, dict) else {}
                except ImportError:
                    logging.warning("tomllib / toml not installed")
                    return {}
        return {}

    def _build_config(self, data: dict[str, Any]) -> AgentConfig:
        """Build AgentConfig from parsed data."""
        # Build rate limit config
        rate_limit = None
        if 'rate_limit' in data:
            rl_data = data['rate_limit']
            rate_limit = RateLimitConfig(
                requests_per_second=rl_data.get('requests_per_second', 10.0),
                requests_per_minute=rl_data.get('requests_per_minute', 60),
                burst_size=rl_data.get('burst_size', 10),
                cooldown_seconds=rl_data.get('cooldown_seconds', 1.0)
            )

        # Build plugin configs
        plugins: list[AgentPluginConfig] = []
        for plugin_data in cast(list[dict[str, Any]], data.get('plugins', [])):
            plugins.append(AgentPluginConfig(
                name=plugin_data.get('name', 'unknown'),
                module_path=plugin_data.get('module_path', ''),
                entry_point=plugin_data.get('entry_point', 'run'),
                enabled=plugin_data.get('enabled', True),
                config=plugin_data.get('config', {})
            ))

        return AgentConfig(
            repo_root=data.get('repo_root', '.'),
            agents_only=data.get('agents_only', False),
            max_files=data.get('max_files'),
            loop=data.get('loop', 1),
            dry_run=data.get('dry_run', False),
            no_git=data.get('no_git', False),
            verbosity=data.get('verbosity', 'normal'),
            rate_limit=rate_limit,
            plugins=plugins,
            selective_agents=data.get('selective_agents', []),
            timeout_per_agent=data.get('timeout_per_agent', {}),
            enable_async=data.get('enable_async', False),
            enable_multiprocessing=data.get('enable_multiprocessing', False),
            max_workers=data.get('workers', data.get('max_workers', 4)),
            strategy=data.get('strategy', 'direct'),
            enable_file_locking=data.get('enable_file_locking', False),
            incremental=data.get('incremental', False),
            graceful_shutdown=data.get('graceful_shutdown', False),
            health_check=data.get('health_check', False),
            resume=data.get('resume', False),
            diff_preview=data.get('diff_preview', False),
            webhook=data.get('webhook', []),
            models=data.get('models', {})
        )

    @staticmethod
    def find_config_file(repo_root: Path) -> Path | None:
        """Find configuration file in repository.

        Args:
            repo_root: Repository root directory.

        Returns:
            Path to config file if found, None otherwise.
        """
        config_names = [
            'agent.yaml', 'agent.yml', 'agent.toml', 'agent.json',
            '.agent.yaml', '.agent.yml', '.agent.toml', '.agent.json',
            'agent_config.yaml', 'agent_config.json'
        ]

        for name in config_names:
            config_path = repo_root / name
            if config_path.exists():
                logging.info(f"Found config file: {config_path}")
                return config_path

        return None
