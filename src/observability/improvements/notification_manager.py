#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Notification Manager - Facade for core notification utilities

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import the facade where a stable public API is desired:
  from notification_manager import NotificationManager
- Or reference the underlying implementation directly:
  from src.core.base.common.utils.notification_manager import NotificationManager

WHAT IT DOES:
- Provides a thin, single-point-of-entry facade that re-exports the NotificationManager implementation from src.core.base.common.utils.notification_manager so callers import from a stable module path.
- Encapsulates the concrete notification implementation behind a module-level shim to simplify imports and allow future refactoring of the underlying implementation without changing callers.

WHAT IT SHOULD DO BETTER:
- Include module-level docstring describing intended lifecycle, thread/async safety, and configuration expectations for NotificationManager.
- Offer versioning or a compatibility wrapper if the underlying implementation changes shape (constructor args or method signatures).
- Add minimal runtime validation or lazy-loading to fail fast if the underlying module is unavailable, and add unit tests and usage examples to clarify intended usage patterns (sync vs async, singleton vs per-agent instances).

FILE CONTENT SUMMARY:
Manager for improvement notifications.
(Facade for src.core.base.common.utils.notification_manager)

from src.core.base.common.utils.notification_manager import NotificationManager

__all__ = ["NotificationManage"""r"]"
from src.core.base.common.utils.notification_manager import NotificationManager

__all__ = ["NotificationManager"]"