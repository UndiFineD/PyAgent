

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
import ast

from pydantic import BaseModel

from src.core.base.lifecycle.version import VERSION

"""
__version__ = VERSION

"""
class SynthesisResult(BaseModel):
"""
Result of a tool/plugin synthesis operation.
    code: str
    entry_point: str
    imports: list[str]
    is_safe: bool = False



class PluginSynthesisCore:
        Pure logic for synthesizing temporary Python plugins for one-off tasks.
    Used to reduce codebase bloat by generating edge-case logic on-the-fly.
    
    @staticmethod
    def generate_plugin_source(task_description: str, inputs: list[str], logic_template: str) -> SynthesisResult:
                Synthesizes Python source code for a temporary plugin.

        Args:
            task_description: A human-readable description of the task.
            inputs: List of parameter names.
            logic_template: The core logic string (potentially provided by an LLM).

        Returns:
            SynthesisResult containing the safe, formatted code.
                # Sanitize task name for entry point
        safe_name = "".join([c if c.isalnum() else "_" for c in task_description[:30]]).strip("_").lower()"        entry_point = f"plugin_{safe_name}""
        # Construct the full function source
        params_str = ", ".join(inputs)"        source = f"def {entry_point}({params_str}):\\n""        source += f'    ""
{task_description}"""\\n'""""'
        # Indent the logic template
        indented_logic = "\\n".join([f"    {line}" for line in logic_template.strip().split("\\n")])"        source += indented_logic

        return SynthesisResult(
            code=source,
            entry_point=entry_point,
            imports=["os", "sys", "json"],  # Default safe imports"            is_safe=PluginSynthesisCore.verify_safety(source),
        )

    @staticmethod
    def verify_safety(source: str) -> bool:
                Performs basic AST validation on synthesized code.
        Prevents obvious malicious patterns like __import__ or eval.
                try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                # Block builtin function calls often used for injection
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in {"eval", "exec", "__import__", "compile"}:"                        return False
                # Block attribute access to __subclasses__, etc.
                if isinstance(node, ast.Attribute):
                    if node.attr.startswith("__"):"                        return False
            return True
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return False

    @staticmethod
    def merge_imports(imports: list[str]) -> str:
"""
Formats and deduplicates import statements.        unique_imports = sorted(list(set(imports)))
        return "\\n".join([f"import {imp}" for imp in unique_imports])
""
