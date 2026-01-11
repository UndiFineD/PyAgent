#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Any, Dict

class EnvironmentDetector:
    """Detects and reports test environment information."""

    def detect(self) -> Dict[str, Any]:
        """Detect environment information."""
        import platform
        import os
        is_ci = any(
            env in os.environ
            for env in ['CI', 'CONTINUOUS_INTEGRATION', 'BUILD_ID', 'GITHUB_ACTIONS']
        )
        system = platform.system().lower()
        if system == 'windows':
            os_name = 'windows'
        elif system == 'darwin':
            os_name = 'darwin'
        elif system == 'linux':
            os_name = 'linux'
        else:
            os_name = 'unknown'
        return {
            'is_ci': is_ci,
            'os': os_name,
            'python_version': platform.python_version(),
            'platform': system
        }
