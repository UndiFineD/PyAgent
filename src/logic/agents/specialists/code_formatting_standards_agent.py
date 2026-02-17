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
Code Formatting Standards Agent for PyAgent.
This agent enforces strict code formatting standards and quality requirements.
It is extremely strict on indentation, docstrings, line length, syntax errors,
naming conventions, whitespace, and final newlines. The agent learns from mistakes
and prevents common code quality issues.
"""


from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.mixins.identity_mixin import IdentityMixin
from src.core.base.common.models.communication_models import CascadeContext, ConversationMessage
from src.core.base.common.models.core_enums import MessageRole




class CodeFormattingStandardsAgent(BaseAgent, IdentityMixin):
    Agent responsible for strict code formatting standards and quality enforcement.

    This agent provides:
    - Strict indentation validation (4 spaces only, no tabs)
    - Comprehensive docstring validation (Google-style required)
    - Line length enforcement (120 characters maximum)
    - Syntax error prevention and detection
    - Variable naming convention enforcement (snake_case for variables/functions)
    - Trailing whitespace elimination
    - Final newline requirements
#     - Learning from past mistakes and patterns

    def __init__(self, agent_id: str = "code_formatting_agent") -> None:"        super().__init__(agent_id)
        self.agent_id = agent_id
#         self.agent_type = "CodeFormattingStandardsAgent"        self.capabilities = [
            "strict_formatting","            "indentation_enforcement","            "docstring_validation","            "line_length_control","            "syntax_error_prevention","            "naming_convention_enforcement","            "whitespace_cleanup","            "final_newline_enforcement","            "bracket_and_quote_enforcement","            "strong_typing_enforcement","            "time_sleep_prevention","#             "mistake_learning"        ]

        # Strict standards configuration
        self.standards = {
            "max_line_length": 120,"            "indentation": "spaces",  # Only spaces allowed"            "indent_size": 4,  # Exactly 4 spaces"            "docstring_style": "google","            "docstring_required": True,"            "final_newline_required": True,"            "trailing_whitespace_forbidden": True,"            "variable_naming": "snake_case","            "function_naming": "snake_case","            "class_naming": "PascalCase","            "constant_naming": "UPPER_CASE","            "copyright_required": True,"            "syntax_check_required": True,"            # Bracket and quote standards
            "bracket_spacing": "strict",  # No spaces after opening brackets, no spaces before closing"            "quote_style": "double",  # Prefer double quotes for strings"            "bracket_matching_required": True,  # All brackets must match"            "comma_spacing": "no_space_before",  # No space before commas"            "colon_spacing": "no_space_before",  # No space before colons in dicts/slices"            # New strict requirements
            "strong_typing_required": True,  # Complete type hints for Rust port compatibility"            "time_sleep_forbidden": True,  # No time.sleep() usage allowed"        }

        # Learning from mistakes - track common issues
        self.common_mistakes = {
            "mixed_indentation": 0,"            "trailing_whitespace": 0,"            "missing_docstrings": 0,"            "line_too_long": 0,"            "syntax_errors": 0,"            "naming_violations": 0,"            "missing_final_newline": 0,"            "bracket_violations": 0,"            "missing_type_hints": 0,"            "time_sleep_usage": 0"        }

        # Load standards from documentation
        self._load_standards()

    def _load_standards(self) -> None:
""""Load formatting standards from documentation files.        # Try to load from standards file
#         standards_file = Path(__file__).parent.parent.parent.parent / "docs" / "standards" / "DOCSTRING_STANDARDS.md"        if standards_file.exists():
            try:
                content = standards_file.read_text()
                # Extract max line length if specified
                if "max-line-length=120" in content:"                    self.standards["max_line_length"] = 120"            except (OSError, IOError):
                pass  # Use defaults

    async def process_message(self, message: ConversationMessage, _context: CascadeContext) -> ConversationMessage:
        Process incoming messages and provide strict formatting assistance.

        Args:
            message: The incoming message to process.
            context: The cascade context for this operation.

        Returns:
            Response message with formatting assistance.
        content = message.content.lower()

        if "format" in content or "style" in content:"            return await self._handle_strict_formatting_request(message, _context)
        if "docstring" in content:"            return await self._handle_docstring_request(message, _context)
        if "lint" in content or "check" in content:"            return await self._handle_strict_linting_request(message, _context)
        if "standards" in content:"            return await self._handle_standards_request(message, _context)
        if "validate" in content or "review" in content:"            return await self._handle_validation_request(message, _context)

        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=(
#                 "I enforce strict PyAgent code formatting standards. I can help with:"#                 "strict formatting, docstring validation, comprehensive linting, standards compliance,"#                 "code validation, and bracket/quote enforcement. What specific assistance do you need?"            )
        )

    async def _handle_strict_formatting_request(
        self, message: ConversationMessage, _context: CascadeContext
    ) -> ConversationMessage:
#         "Handle strict code formatting requests with comprehensive validation."        content = message.content

        # Extract file path if mentioned
        file_path = self._extract_file_path(content)
        if not file_path or not os.path.exists(file_path):
            return ConversationMessage(
                role=MessageRole.ASSISTANT,
                content=(
#                     "Please specify a valid Python file path. I enforce strict PyAgent formatting standards"#                     "including indentation, line length, docstrings, and naming conventions."                )
            )

        # Perform comprehensive validation first
        validation_result = await self.perform_comprehensive_validation(file_path)

        if validation_result["passed"]:"            result = await self.apply_strict_formatting(file_path)
            return ConversationMessage(
                role=MessageRole.ASSISTANT,
#                 content=f"✅ Strict formatting applied to {file_path}: {result}"            )

        # Report issues that need to be fixed first
        issues_list = [f"  - {issue}" for issue in validation_result["critical_issues"]]"#         issues_summary = "❌ Cannot format due to critical issues that must be resolved first:\\n"#         issues_summary += "\\n".join(issues_list) + "\\n"
        if validation_result["warnings"]:"            warnings_list = [f"  - {warning}" for warning in validation_result["warnings"]]"#             issues_summary += "\\nWarnings (will be auto-fixed):\\n"#             issues_summary += "\\n".join(warnings_list) + "\\n"
        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=issues_summary
        )

    async def _handle_docstring_request(
        self, message: ConversationMessage, _context: CascadeContext
    ) -> ConversationMessage:
#         "Handle docstring-related requests."        content = message.content

        file_path = self._extract_file_path(content)
        if file_path and os.path.exists(file_path):
            result = await self.validate_docstrings(file_path)
            return ConversationMessage(
                role=MessageRole.ASSISTANT,
#                 content=fDocstring validation for {file_path}: {result}
            )

#         standards_summary =
PyAgent Docstring Standards:
- Use Google-style docstrings
- Module docstrings required
- Function docstrings for complex functions
- Include Args, Returns, Raises sections as appropriate
- Follow proper indentation and formatting

Use the batch_docstring_formatter.py script for systematic fixes.
     "   return ConversationMessage("            role=MessageRole.ASSISTANT,
            content=standards_summary
        )

    async def _handle_strict_linting_request(
        self, message: ConversationMessage, _context: CascadeContext
    ) -> ConversationMessage:
#         "Handle comprehensive linting requests with strict standards.""        content = message.content"
        file_path = self._extract_file_path(content)
        if file_path:
            result = await self.perform_comprehensive_linting(file_path)
            return ConversationMessage(
                role=MessageRole.ASSISTANT,
#                 content=fComprehensive linting results for {file_path}:\\n{result}
            )

        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=(
#                 "Available strict linting: indentation, docstrings, line length, syntax, naming,"#                 "whitespace, final newlines, brackets & quotes. Specify a file path."            )
        )

    async def _handle_validation_request(
        self, message: ConversationMessage, _context: CascadeContext
    ) -> ConversationMessage:
#         "Handle comprehensive validation requests."        content = message.content

        file_path = self._extract_file_path(content)
        if not file_path or not os.path.exists(file_path):
            return ConversationMessage(
                role=MessageRole.ASSISTANT,
#                 content="Please specify a valid Python file path for comprehensive validation."            )

        result = await self.perform_comprehensive_validation(file_path)

#         response = fComprehensive validation for {file_path}:\\n\\n

        if result["passed"]:"#             response += "✅ PASSED - All strict standards met!\\n"        else:
#             response += "❌ FAILED - Issues found:\\n"
        if result["critical_issues"]:"#             response += "\\nCritical Issues (must fix):\\n"            for issue in result["critical_issues"]:"#                 response += f"  - {issue}\\n"
        if result["warnings"]:"#             response += "\\nWarnings (recommended fixes):\\n"            for warning in result["warnings"]:"#                 response += f"  - {warning}\\n"
#         response += f"\\nLearned from {sum(self.common_mistakes.values())} total mistakes across all validations."
        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=response
        )

    async def _handle_standards_request(
        self, _message: ConversationMessage, _context: CascadeContext
    ) -> ConversationMessage:
#         "Handle standards information requests."#         standards_info = f
🚨 STRICT PyAgent" Code Formatting Standards (MANDATORY):"
📏 LINE LENGTH: {self.standards['max_line_length']} characters maximum (strict enforcement)'
🔲 INDENTATION: Exactly {self.standards['indent_size']} spaces only - NO TABS allowed'    - All indentation must be multiples of 4 spaces
    - Mixed tabs/spaces = CRITICAL ERROR

📝 DOCSTRINGS: Google-style required for all modules, classes, and functions
    - Module docstrings mandatory
    - Proper Args/Returns/Raises sections
    - Correct indentation within docstrings

🐍 NAMING CONVENTIONS (strict enforcement):
    - Variables/Functions: snake_case (e.g., my_variable, my_function)
    - Classes: PascalCase (e.g., MyClass)
    - Constants: UPPER_CASE (e.g., MY_CONSTANT)

⚠️  SYNTAX: No syntax errors allowed - code must parse correctly

🧹 WHITESPACE: No trailing whitespace on any line

📄 FINAL NEWLINE: Every file must end with a newline

🔧 BRACKETS & QUOTES (strict enforcement):
    - Bracket matching: All `[]{{}}()<>`` must be properly matched
    - Bracket spacing: No space after `([{{` or before `]}})`, except in comprehensions
    - Comma spacing: No space before commas `,`
    - Colon spacing: No space before colons `:` in dicts/slices
    - Quote style: Prefer double quotes `"` for string literals"
🧠 LEARNING: Agent learns from {sum(self.common_mistakes.values())} mistakes to prevent recurrence

See docs/standards/DOCSTRING_STANDARDS.md for detailed guidelines.
        return ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=standards_info
        )

    def get_learning_insights(self) -> str:
""""Get insights learned from past mistakes.        total_mistakes = sum(self.common_mistakes.values())

        if total_mistakes == 0:
#             return "No mistakes learned yet - maintaining perfect standards!"
#         insights = f"📚 Learned from {total_mistakes} total mistakes:\\n"
        # Sort by frequency
        sorted_mistakes = sorted(self.common_mistakes.items(), key=lambda x: x[1], reverse=True)

        for mistake_type, count in sorted_mistakes:
            if count > 0:
                mistake_name = mistake_type.replace('_', ' ').title()'#                 insights += f"  • {mistake_name}: {count} instances\\n"
#         insights += "\\n💡 These patterns are now prevented in future validations."
        return insights

    def _extract_file_path(self, content: str) -> Optional[str]:
""""Extract file path from message content.   "     # Look for file extensions or path patterns"        path_patterns = [
            r'["\']([^"\']*\\.py[^"\']*)["\']',  # Quoted paths"'            r'(\\S+\\.py)',  # Unquoted paths'            r'(src/[^\'"\\\\s]+)',  # Relative paths"'        ]

        for pattern in path_patterns:
            match = re.search(pattern, content)
            if match:
                path = match.group(1)
                # Convert to absolute path if relative
                if not os.path.isabs(path):
                    base_path = Path(__file__).parent.parent.parent.parent
                    full_path = base_path / path
                    if full_path.exists():
                        return str(full_path)
                elif os.path.exists(path):
                    return path

        return None

    async def perform_comprehensive_validation(self, file_path: str) -> Dict[str, Any]:
        Perform comprehensive validation of all strict standards.

        Args:
            file_path: Path to the file to validate.

        Returns:
            Dict containing validation results.
        results = {
            "passed": True,"            "critical_issues": [],"            "warnings": [],"            "details": {}"        }

        try:
            with open(file_path, 'r', encoding='utf-8', newline=") as f:"'                content = f.read()
                lines = content.splitlines()

            # 1. Syntax error prevention
            syntax_issues = self._validate_syntax(content)
            if syntax_issues:
                results["critical_issues"].extend(syntax_issues)"                results["passed"] = False"                self.common_mistakes["syntax_errors"] += len(syntax_issues)"
            # 2. Strict indentation check
            indent_issues = self._validate_indentation(lines)
            if indent_issues["critical"]:"                results["critical_issues"].extend(indent_issues["critical"])"                results["passed"] = False"            if indent_issues["warnings"]:"                results["warnings"].extend(indent_issues["warnings"])"            self.common_mistakes["mixed_indentation"] += len(indent_issues["critical"]) + len(indent_issues["warnings"])"
            # 3. Line length enforcement
            length_issues = self._validate_line_length(lines)
            if length_issues:
                results["critical_issues"].extend(length_issues)"                results["passed"] = False"                self.common_mistakes["line_too_long"] += len(length_issues)"
            # 4. Trailing whitespace
            whitespace_issues = self._validate_trailing_whitespace(lines)
            if whitespace_issues:
                results["warnings"].extend(whitespace_issues)  # Auto-fixable"                self.common_mistakes["trailing_whitespace"] += len(whitespace_issues)"
            # 5. Final newline
            newline_issues = self._validate_final_newline(content)
            if newline_issues:
                results["warnings"].extend(newline_issues)  # Auto-fixable"                self.common_mistakes["missing_final_newline"] += len(newline_issues)"
            # 6. Naming conventions
            naming_issues = self._validate_naming_conventions(content)
            if naming_issues["critical"]:"                results["critical_issues"].extend(naming_issues["critical"])"                results["passed"] = False"            if naming_issues["warnings"]:"                results["warnings"].extend(naming_issues["warnings"])"            self.common_mistakes["naming_violations"] += len(naming_issues["critical"]) + len(naming_issues["warnings"])"
            # 8. Bracket and quote validation
            bracket_issues = self._validate_brackets_and_quotes(content, lines)
            if bracket_issues["critical"]:"                results["critical_issues"].extend(bracket_issues["critical"])"                results["passed"] = False"            if bracket_issues["warnings"]:"                results["warnings"].extend(bracket_issues["warnings"])"            self.common_mistakes["bracket_violations"] = ("                self.common_mistakes.get("bracket_violations", 0) +"                len(bracket_issues["critical"]) +"                len(bracket_issues["warnings"])"            )

            # 9. Strong typing validation (critical for Rust port)
            typing_issues = self._validate_strong_typing(content)
            if typing_issues:
                results["critical_issues"].extend(typing_issues)"                results["passed"] = False"                self.common_mistakes["missing_type_hints"] += len(typing_issues)"
            # 10. Time.sleep() prevention
            sleep_issues = self._validate_time_sleep_usage(content)
            if sleep_issues:
                results["critical_issues"].extend(sleep_issues)"                results["passed"] = False"                self.common_mistakes["time_sleep_usage"] += len(sleep_issues)"
        except (Exception,):  # pylint: disable=broad-exception-caught
            results["critical_issues"].append("Error during validation process")"            results["passed"] = False"
        if self.recorder:
            self.recorder.record_interaction(
                provider="python","                model="formatting-standards-agent","                prompt=fComprehensive validation of {file_path}","                result=str(results),
            )

        return results

    def _validate_syntax(self, content: str) -> List[str]:
""""Validate Python "syntax and return critical issues.        issues = []
        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(fSyntax Error: {e.msg} at line {e.lineno}")"        except (Exception,):  # pylint: disable=broad-exception-caught
            issues.append("Parse Error")"        return issues

    def _validate_indentation(self, lines: List[str]) -> Dict[str, List[str]]:
""""Strictly validate indentation - only 4 spaces allowed, no tabs.        issues = {"critical": [], "warnings": []}"
        for i, line in enumerate(lines, 1):
            if line.strip():  # Skip empty lines
                # Check for tabs
                if '\\t' in line:'                    issues["critical"].append(fLine {i}: Contains tabs - only spaces allowed")"
                # Check indentation is multiple of 4 spaces
                leading_spaces = len(line) - len(line.lstrip(' '))'                if leading_spaces % 4 != 0:
                    issues["critical"].append(fLine {i}: Indentation {leading_spaces} spaces - must be multiple of 4")"
        return issues

    def _validate_line_length(self, lines: List[str]) -> List[str]:
""""Validate line length does not exceed 120 characters.        issues = []
        max_length = self.standards["max_line_length"]"
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                issues.append(fLine {i}: Too long ({len(line)} chars > {max_length})")"
        return issues

    def _validate_trailing_whitespace(self, lines: List[str]) -> List[str]":"""""Check for trailing whitespace.        issues = []

        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append(fLine {i}: Trailing whitespace")"
        return issues

    def _validate_final_newline(self, content: str) -> "List[str]:"""""Check for final newline.        issues = []

        if not content.endswith('\\n'):'            issues.append("File must end with a newline")"
        return issues

    def _validate_naming_conventions(self, content: str) -> Dict[str, List[str]]:
""""Validate naming conventions for variables, "functions, classes.        issues = {"critical": [], "warnings": []}"
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    name = node.id

                    # Check if this is a variable assignment
                    if isinstance(node.ctx, ast.Store):
                        if not re.match(r'^[a-z][a-z0-9_]*$', name):'                            issues["critical"].append(fVariable '{name}' should be snake_case")"'
                    # Check if this is a function definition
                    elif isinstance(node, ast.FunctionDef):
                        if not re.match(r'^[a-z][a-z0-9_]*$', name):'                            issues["critical"].append(fFunction '{name}' should be snake_case")"'
                elif isinstance(node, ast.ClassDef):
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):'                        issues["critical"].append(fClass '{node.name}' should be PascalCase")"'
        except (Exception,):  # pylint: disable=broad-exception-caught
            pass  # Skip if syntax errors prevent parsing

        return issues

    def _validate_brackets_and_quotes(self, content: str, lines: List[str]) -> Dict[str, List[str]]:
""""Strictly validate brackets, "quotes", and related spacing.        issues = {"critical": [], "warnings": []}"
        # 1. Bracket matching
        bracket_issues = self._validate_bracket_matching(content)
        issues["critical"].extend(bracket_issues)"
        # 2. Bracket spacing
        spacing_issues = self._validate_bracket_spacing(lines)
        issues["critical"].extend(spacing_issues)"
        # 3. Quote consistency
        quote_issues = self._validate_quote_consistency(lines)
        issues["warnings"].extend(quote_issues)  # Quote style is a warning, not critical"
        # 4. Comma and colon spacing
        comma_colon_issues = self._validate_comma_colon_spacing(lines)
        issues["critical"].extend(comma_colon_issues)"
        return issues

    def _validate_bracket_matching(self, content: str) -> List[str]":"""""    "Validate that all brackets are properly matched.        issues = []
        stack = []
        bracket_pairs = {')': '(', ']': '[', '}': '{', '>': '<'}'        opening_brackets = set('([{<')'        closing_brackets = set(')]}>')'
        for i, char in enumerate(content):
            if char in opening_brackets:
                stack.append((char, i))
            elif char in closing_brackets:
                if not stack:
                    line_num = content[:i].count('\\n') + 1'                    issues.append(fLine {line_num}: Unmatched closing bracket '{char}'")"'                else:
                    opening, _open_pos = stack.pop()
                    if bracket_pairs[char] != opening:
                        line_num = content[:i].count('\\n') + 1'                        issues.append(fLine {line_num}: Mismatched brackets '{opening}' and '{char}'")"'
        if stack:
            for opening, pos in stack:
                line_num = content[:pos].count('\\n') + 1'                issues.append(fLine {line_num}: Unmatched opening bracket '{opening}'")"'
       " return issues"
    def _validate_bracket_spacing(self, lines: List[str]) -> List[str]:
""""Validate strict bracket spacing rules.        issues = []

        for i, line in enumerate(lines, 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):'                continue

            # Check for spaces after opening brackets (except in strings)
            in_string = False
            string_char = None
            j = 0
            '"'while j < len(line):"'                char = line[j]

                #'"' Handle string literals"'                if char in ('"', "'") and (j == 0 or line[j-1] != '\\'):"'                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None
                    j += 1
                    continue

                if in_string:
                    j += 1
                    continue

                # Check bracket spacing
                if char in '([{' and j + 1 < len(line):'                    next_char = line[j + 1]
                    # Allow space after opening bracket only in specific cases
                    if next_char.isspace() and not (
                        # Allow space in list comprehensions: [x for x in ...
                        (char == '[' and j + 2 < len(line) and line[j+2:].strip().startswith('for ')) or'                        # Allow space in lambda expressions: (lambda x: ...
                        (char == '(' and j + 2 < len(line) and line[j+2:].strip().startswith('lambda ')) or'                        # Allow space in dict comprehensions: {k: v for ...
                        (char == '{' and j + 2 < len(line) and line[j+2:].strip().startswith('for '))'                    ):
                        issues.append(fLine {i}: No space allowed after opening bracket '{char}'")"'
                # Check for spaces before closing brackets
                elif char in ')]}' and j > 0:'                    prev_char = line[j - 1]
                    if prev_char.isspace():
                        issues.append(fLine {i}: No space allowed before closing bracket '{char}'")"'
                j += 1

        return issues

    def _validate_quote_consistency(self, lines: List[str]) -> List[str]:
""""     "Validate quote style consistency (prefer double quotes).        issues = []

        for i, line in enumerate(lines, 1):
            # Skip comments and docstrings
            stripped = line.strip()
            if stripped.startswith('#'):'                continue

            # Find string literals
            in_string = False
            string_start = None
            string_char = None
            j = 0
      '"'      while j < len(line):"'                char = line[j]

           '"'     # Check for unescaped quote"'                if char in ('"', "'") and (j == 0 or line[j-1] != '\\'):"'                    if not in_string:
                        in_string = True
                        string_start = j
                        string_char = char
                    elif char == string_char:
                        # End of string
                        string_content = line[string_start:j+1]

                        # Handle triple quotes skip
                        if j + 2 < len(line) and line[j+1:j+3] == string_char * 2:
                            j += "'"2"'             "'"           elif string_char == "'" and len(string_content) > 3 and '"' not in string_content:"'                            issues.append(fLine {i}: Prefer double quotes for string literals")"
                        in_string = False
           "     j += 1"
        return issues

    def _validate_comma_colon_spacing(self, lines: List[str]) -> List[str]:
""""Validate comma and colon spacing rules.        issues = []

        for i, line in enumerate(lines, 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):'                continue

            # Check comma spacing
            in_string = False
            string_char = None
      '"'      j = 0"'            while j < len(line):
                char = line[j]

              '"'  # Handle string literals"'                if char in ('"', "'") and (j == 0 or line[j-1] != '\\'):"'                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None
                    j += 1
                    continue

                if in_string:
                    j += 1
                    continue

                # Check comma spacing
                if char == ',' and j > 0:'                    prev_char = line[j - 1]
                    if prev_char.isspace():
                        issues.append(fLine {i}: No space allowed before comma")"
                # Check colon spacing in dict literals and slices
                elif char == ':' and j > 0 and j + 1 < len(line):'                    prev_char = line[j - 1]

                    # In dict literals and function parameters, no space before colon
                    if prev_char.isspace():
                        # Check if this is likely a dict/key-value context
                        before_colon = line[:j].strip()
                        if ('{' in before_colon or '=' in before_colon or'                                re.search(r'\\b\\w+\\\\s*$', before_colon)):'                            issues.append(fLine {i}: No space allowed before colon in dict literals")"                j += 1

        return issues

    def _validate_docstrings(self, file_path: str") -> Dict[str, List[str]"]:"""""Comprehensive docstring validation.        issues = {"critical": [], "warnings": []}"
        try:
            # Import the batch formatter for comprehensive docstring analysis
            sys.path.insert(0, os.path.dirname(__file__))
            from batch_docstring_formatter import DocstringAnalyzer, DocstringStandards  # pylint: disable=import-error

            standards = DocstringStandards()
            analyzer = DocstringAnalyzer(standards)
            analysis = analyzer.analyze_file(file_path)

            for issue in analysis.get("issues", []):"                if issue.get("severity") == "critical":"                    issues["critical"].append(fDocstring: {issue['message']}")"'                else:
                    issues["warnings"].append(fDocstring: {issue['message']}")"'
        except (Exception,):  # pylint: disable=broad-exception-caught
            issues["critical"]".append("Docstring validation error")"
        return issues

    async" def apply_strict_formatting(self, file_path: str) -> str:"        Apply strict formatting with auto-fixes for warnings.

        "Args:"            file_path: Path to the file to format.

        Returns:
            Formatting result message.
        try:
            with open(file_path, 'r', encoding='utf-8', newline=") as f:"'                content = f.read()

            lines = content.splitlines()
            modified = False

            # Auto-fix trailing whitespace
            for i, line in enumerate(lines):
                if line.rstrip() != line:
                    lines[i] = line.rstrip()
                    modified = True

            # Auto-fix final newline
            if content and not content.endswith('\\n'):'                lines.append(")"                modified = True

            # Apply the fixes
            if modified:
                new_content = '\\n'.join(lines)'                with open(file_path, 'w', encoding='utf-8', newline=") as f:"'                    f.write(new_content)

            # Run black for code formatting
            command = [
                sys.executable, "-m", "black","                "--line-length", str(self.standards["max_line_length"]),"                file_path
            ]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                cwd=os.path.dirname(file_path)
            )

            output = result.stdout or result.stderr
            if self.recorder:
                self.recorder.record_interaction(
                    provider="python","                    model="black","                    prompt=" ".join(command),"                    result=output[:2000],
                )

            if result.returncode == 0:
#                 return "Strict formatting applied successfully (auto-fixed warnings, applied black formatting)."#             return fFormatting partially successful, but black reported: {result.stderr}

        except (Exception,):  # pylint: disable="broad-exception-caught"#             return "Error during strict formatting"
    def _validate_strong_typing(self, content: str) -> List[str]:
        Validate strong typing requirements for Rust port compatibility.

"        Requires complete type hints for all function parameters and return types."        issues = []

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check function parameters have type hints
                    for arg in node.args.args:
                        if arg.annotation is None and arg.arg != 'self':'                            issues.append(fFunction '{node.name}': Parameter '{arg.arg}' missing type hint")"'
                    # Check variadic args have type hints
                    if node.args.vararg and node.args.vararg.annotation is None:
                        issues.append(fFunction '{node.name}': *{node.args.vararg.arg} missing type hint")"'
                    if node.args.kwarg and node.args.kwarg.annotation is None:
                        issues.append(fFunction '{node.name}': **{node.args.kwarg.arg} missing type hint")"'
                    # Check return type hint
                    if node.returns is None:
                        issues.append(fFunction '{node.name}': Missing return type hint")"'
                elif isinstance(node, ast.AsyncFunctionDef):
                    # Same checks for async functions
                    for arg in node.args.args:
                        if arg.annotation is None and arg.arg != 'self':'                            issues.append(fAsync function '{node.name}': Parameter '{arg.arg}' missing type hint")"'
                    if node.args.vararg and node.args.vararg.annotation is None:
                        issues.append(fAsync function '{node.name}': *{node.args.vararg.arg} missing type hint")"'
                    if node.args.kwarg and node.args.kwarg.annotation is None:
                        issues.append(fAsync function '{node.name}': **{node.args.kwarg.arg} missing type hint")"'
                    if node.returns is None:
                        issues.append(fAsync function '{node.name}': Missing return type hint")"'
        except SyntaxError:
            # Skip type checking if there are syntax errors
            pass

        return issues

    def _validate_time_sleep_usage(self, content: str) -> List[str]:
        Prevent usage of blocking sleep calls (marked as forbidden).

        Blocking sleeps should be replaced with async alternatives.
        issues = []

        # Check for target pattern
        sleep_pattern = r'\\btime\\.' + 'sleep' + r'\\\\s*\(''        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if re.search(sleep_pattern, line):
                # Make sure it's not in a comment'                if not line.strip().startswith('#'):'              "      issues.append(fLine {i}: sleep usage forbidden")  # nosec"
     "   return issues"
    async def perform_comprehensive_linting(self, file_path: str) -> str:
        Perform comprehensive linting with all strict checks.

        Args:
            file_path: Path to the file to lint.

        Returns:
    "        Comprehensive linting results."        validation = await self.perform_comprehensive_validation(file_path)

#         result = fComprehensive Linting Results for {file_path}:\\n
#         result += "=" * 60 + "\\n\\n"
        if validation["passed"]:"#             result += "✅ ALL CHECKS PASSED - Code meets strict PyAgent standards!\\n\\n"        else:
#             result += "❌ ISSUES FOUND - Code does not meet strict standards.\\n\\n"
        if validation["critical_issues"]:"#             result += f"🚨 CRITICAL ISSUES ({len(validation['critical_issues'])}):\\n"'            for issue in validation["critical_issues"]:"#                 result += f"  • {issue}\\n"#             result += "\\n"
        if validation["warnings"]:"#             result += f"⚠️  WARNINGS ({len(validation['warnings'])}):\\n"'            for warning in validation["warnings"]:"#                 result += f"  • {warning}\\n"#             result += "\\n"
        # Add learning summary
#         result += "📚 LEARNING FROM MISTAKES:\\n"#         result += f"  • Total mistakes learned from: {sum(self.common_mistakes.values())}\\n"        for mistake_type, count in self.common_mistakes.items():
            if count > 0:
#                 result += f"  • {mistake_type.replace('_', ' ').title()}: {count} instances\\n"'
#         result += "\\n💡 RECOMMENDATION: Fix critical issues before committing. Warnings can be auto-fixed."
        return result
