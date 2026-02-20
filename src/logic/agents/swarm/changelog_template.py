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
"""
Changelog Template - Template configuration dataclass
[Brief Summary]
A small, focused dataclass that models configuration for generating human-readable changelogs; intended as a lightweight, serializable template used by changelog generation code.
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ChangelogTemplate(name="MyProject", project_type="library", sections=["Added","Changed","Fixed"], header_format="## [{version}] - {date}", include_links=True)"- Pass the instance to a changelog renderer/generator which iterates sections and fills header_format with version/date and optionally appends links and contributors.
WHAT IT DOES:
- Encapsulates name, project_type, ordered sections, header format and toggles for links and contributor lists.
- Provides a single source of truth for formatting options consumed by changelog-generation logic.
WHAT IT SHOULD DO BETTER:
- Validate inputs (e.g., non-empty sections, recognized project_type values) and provide helpful error messages.
- Offer serialization helpers (to/from dict or TOML/YAML) and a default set of sensible sections per project_type.
- Include templating hooks or callable formatters for more flexible header/body rendering and i18n support.
FILE CONTENT SUMMARY:
Changelog template.py module.

"""
try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import List
except ImportError:
    from typing import List



@dataclass
class ChangelogTemplate:
""""
Template configuration for generating human-readable changelogs.    name: str
    project_type: str
    sections: List[str]
#     header_format: str = "## [{version}] - {date}"    include_links: bool = True
    include_contributors: bool =" False"
try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import List
except ImportError:
    from typing import List



@dataclass
class ChangelogTemplate:
""""
Template configuration for generating human-readable changelogs. "   name: str"    project_type: str
    sections: List[str]
#     header_format: str = "## [{version}] - {date}"    include_links: bool = True
    include_contributors: bool = False

"""
