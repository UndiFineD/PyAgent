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
LocaleCode - Enum of supported locale strings

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.lifecycle.locale_code import LocaleCode
# Example: LocaleCode.EN_US.value -> "en-US"

WHAT IT DOES:
Provides a small Enum of locale codes used when generating agent reports.

WHAT IT SHOULD DO BETTER:
Document intended package location and add comprehensive locale coverage and unit tests for serialization/deserialization.

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LocaleCode(Enum):
    """Supported locales for reports."""

    EN_US = "en-US"
    DE_DE = "de-DE"
    FR_FR = "fr-FR"
    ES_ES = "es-ES"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LocaleCode(Enum):
    """Supported locales for reports."""

    EN_US = "en-US"
    DE_DE = "de-DE"
    FR_FR = "fr-FR"
    ES_ES = "es-ES"
