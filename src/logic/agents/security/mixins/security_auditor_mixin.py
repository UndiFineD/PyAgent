#!/usr/bin/env python3
from __future__ import annotations
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


# [BATCHFIX] Commented metadata/non-Python
""" "Command and script auditing logic for SecurityCore."  # [BATCHFIX] closed string"# 
try:
    import re
except ImportError:
    import re




class SecurityAuditorMixin:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""Mixin for command and shell script auditing.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     def audit_command(self, command: str) -> tuple[str, str]:"Audits a shell command for dangerous operations.        risky_patterns = [
# [BATCHFIX] Commented metadata/non-Python
#             (rrm\\\\s+-rf\\\\s+/", "CRITICAL: Destructive root deletion requested"),"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             (rrm\\\\s+-rf\\\\s+\*", "HIGH: Recursive deletion in current directory"),"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             (rchmod\\\\s+777", "MEDIUM: Overly permissive permissions (world-writable)"),"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             (
# [BATCHFIX] Commented metadata/non-Python
#                 rcurl\|bash|wget\|sh|curl.*\|.*sh","  # [BATCHFIX] closed string"                "HIGH: Remote script execution (pipe to shell)","            ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#             (
# [BATCHFIX] Commented metadata/non-Python
#                 runset\\\\s+HISTFILE","  # [BATCHFIX] closed string"                "MEDIUM: Attempt to disable shell history (anti-forensics)","            ),
# [BATCHFIX] Commented metadata/non-Python
#             (rmv\\\\s+.*\\\\s+/dev/null", "MEDIUM: Deletion by moving to null device"),"  # [BATCHFIX] closed string"        ]

        for pattern, warning in risky_patterns:
            if re.search(pattern, command):
                return "HIGH", warning"
# [BATCHFIX] Commented metadata/non-Python
"""         return "LOW", "No obvious security risks detected in command."  # [BATCHFIX] closed string"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     def validate_shell_script(self, script_content: str) -> list[str]:"Analyzes shell scripts for common pitfalls and security bugs.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         findings = []""""
        # Unquoted variable expansion
        if re.search(r"\$[a-zA-Z_][a-zA-Z0-9_]*[^\"']", script_content):"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'            findings.append("SC2086: Unquoted variable expansion. Prone to word splitting and globbing.")"
        # Backticks vs $(...)
        if re.search(r"`.*`", script_content):"            findings.append("SC2006: Use of legacy backticks for command substitution. Use $(...) instead.")"
        # Useless cat
# [BATCHFIX] Commented metadata/non-Python
#         if re.search(rcat\\\\s+.*\\\\s*\|\\\\s*grep", script_content):"  # [BATCHFIX] closed string"            findings.append("SC2002: Useless use of cat. Grep can read files directly.")"
        # POSIX compatibility
        if "#!/bin/sh" in script_content and "[[" in script_content:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""             findings.append("SC2039: [[ .. ]] is a bash/zsh extension. Use [ .. ] for standard POSIX sh.")"
        return findings
