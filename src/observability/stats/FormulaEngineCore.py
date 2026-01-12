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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
FormulaEngineCore logic for PyAgent.
Pure logic for safe mathematical evaluation via AST.
No I/O or side effects.
"""



import ast
import operator
import re
from typing import Any, Dict, List, Optional, Type



































class FormulaEngineCore:
    """Pure logic core for formula calculations."""

    def __init__(self) -> None:
        self.operators: Dict[Type[ast.AST], Any] = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise TypeError(f"Constant of type {type(node.value)} is not a number")
        elif hasattr(ast, "Num") and isinstance(node, ast.Num): # type: ignore
             return float(node.n) # type: ignore
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate_logic(self, formula: str, variables: Dict[str, Any]) -> float:
        """Core logic for calculating a formula result."""
        # Handle special functions like AVG
        if "AVG(" in formula:
            match = re.search(r'AVG\(\{(\w+)\}\)', formula)
            if match:
                var_name = match.group(1)
                if var_name in variables:
                    values = variables[var_name]
                    if isinstance(values, list) and values:
                        return sum(values) / len(values)
            return 0.0

        try:
            # Replace {variable} with actual values
            eval_formula = formula
            for var_name, var_value in variables.items():
                eval_formula = eval_formula.replace(f"{{{var_name}}}", str(var_value))
            
            # Use safe AST evaluation
            tree = ast.parse(eval_formula, mode='eval')
            return self._eval_node(tree.body)
        except Exception:
            # Core returns a default value, Shell handles logging
            return 0.0

    def validate_logic(self, formula: str) -> Dict[str, Any]:
        """Core logic for validating formula syntax."""
        try:
            if any(seq in formula for seq in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}

            test_formula = formula
            vars_found: List[str] = re.findall(r'\{(\w+)\}', formula)
            for var in vars_found:
                test_formula = test_formula.replace(f"{{{var}}}", "1")
            
            # Final AST parse check
            ast.parse(test_formula, mode='eval')
            return {"is_valid": True, "error": None}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}
