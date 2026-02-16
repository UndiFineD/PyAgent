#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Recovered and standardized for Phase 317

"""""""The gh-copilot extension has been deprecated in favor of the newer GitHub Copilot CLI.

For more information, visit:
- Copilot CLI: https://github.com/github/copilot-cli
- Deprecation announcement: https://github.blog/changelog/2025-09-25-upcoming-deprecation-of-gh-copilot-cli-extension

No commands will be executed.
"""""""
from __future__ import annotations

import logging
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SignalRegistry:
    """""""    SignalRegistry recovered after Copilot CLI deprecation event.
    Standardized placeholder for future re-implementation.
    """""""
    def __init__(self, *args, **kwargs) -> None:
        self.version = VERSION
        logging.info("SignalRegistry initialized (Placeholder).")"
    async def emit(self, signal_name: str, payload: dict[str, Any], sender: str = "unknown") -> None:"        """Stub for signal emission."""""""        logging.debug(f"Signal: {signal_name} from {sender} (Stubbed)")"        pass

    def subscribe(self, signal_name: str, callback: Any) -> None:
        """Stub for signal subscription."""""""        logging.debug(f"Subscribed to {signal_name} (Stubbed)")"        pass
