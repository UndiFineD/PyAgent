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
LocalizedString - Simple dataclass for locale-aware strings

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from localized_string import LocalizedString
ls = LocalizedString("greeting", {"en": "Hello", "nl": "Hallo"}, default="Hello")
# retrieve with fallback
text = ls.translations.get(user_locale, ls.default)

WHAT IT DOES:
- Encapsulates a translation key with a mapping of locale codes to text and a default fallback string.
- Provides a compact, serializable container suitable for small-scale i18n storage and transfer.
- Exposes attributes key, translations (dict[str, str]) and default for straightforward usage.

WHAT IT SHOULD DO BETTER:
- Add convenience methods (e.g., get(locale, fallback_chain=True), merge(other)) to centralize fallback and merging logic.
- Validate locale keys and types, and enforce immutability or provide controlled mutation APIs.
- Support serialization helpers (to_dict/from_dict), pluralization, formatting placeholders, and unit tests for edge cases.

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

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class LocalizedString:
    """Localized string with translations.
    Attributes:
        key: String key.
        translations: Locale to text mapping.
        default: Default text if locale missing.
    """

    key: str
    translations: dict[str, str] = field(default_factory=dict)  # type: ignore[assignment]
    default: str = ""
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class LocalizedString:
    """Localized string with translations.
    Attributes:
        key: String key.
        translations: Locale to text mapping.
        default: Default text if locale missing.
    """

    key: str
    translations: dict[str, str] = field(default_factory=dict)  # type: ignore[assignment]
    default: str = ""
