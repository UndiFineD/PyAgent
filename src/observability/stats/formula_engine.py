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
#
# you may not use this file except in compliance with the License.
# you may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Formula Engine - Formula processing and calculation

Provides safe AST-based formula parsing, variable substitution for tokens like {var},
a simple AVG aggregate handler, optional Rust acceleration via rust_core, and a small
facade for defining and computing named formulas.
"""

from __future__ import annotations

import ast
import contextlib
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Callable, cast

from src.core.base.common.formula_core import FormulaCore

try:
    from rust_core import rust_core as rc  # type: ignore[import-untyped]
except ImportError:
    rc = None


@dataclass
class FormulaValidation:
    """Result of a formula validation check."""

    is_valid: bool
    error: Optional[str] = None


class FormulaEngineCore(FormulaCore):
    """Extended formula core for observability specific needs (e.g. AVG)."""

    def calculate_logic(self, formula: str, variables: Dict[str, Any]) -> float:
        """Calculate a formula result with optional rust acceleration and simple AVG support."""
        # Prefer Rust acceleration when available and when AVG is not present
        if rc and "AVG(" not in formula:
            with contextlib.suppress(Exception):
                float_vars: Dict[str, float] = {
                    k: float(v) for k, v in variables.items() if isinstance(v, (int, float))
                }
                fn_obj = getattr(rc, "evaluate_formula", None) or getattr(rc, "evaluate_formula_rust", None)
                if fn_obj is None:
                    # No rust-backed evaluator available
                    pass
                else:
                    # Cast to a known callable signature so static checkers accept the call and return type
                    fn = cast(Callable[[str, Dict[str, float]], float], fn_obj)
                    return float(fn(formula, float_vars))

        # Simple AVG aggregate handling: AVG({var})
        if "AVG(" in formula:
            match = re.search(r"AVG\(\{(\w+)\}\)", formula)
            if match:
                var_name = match.group(1)
                if var_name in variables:
                    values = variables[var_name]
                    if isinstance(values, list) and values:
                        numeric = [float(v) for v in values if isinstance(v, (int, float))]
                        if numeric:
                            return sum(numeric) / len(numeric)
            return 0.0

        # Fallback to safe AST-based evaluation via FormulaCore.evaluate
        try:
            # Identify variables used in formula and prepare numeric mapping
            vars_used = re.findall(r"\{(\w+)\}", formula)
            eval_vars: Dict[str, float] = {}
            for name in vars_used:
                if name in variables and isinstance(variables[name], (int, float)):
                    eval_vars[name] = float(variables[name])

            # Core.evaluate expects a formula without braces
            sanitized_formula = formula.replace("{", "").replace("}", "")
            return float(self.evaluate(sanitized_formula, eval_vars))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.debug("FormulaEngineCore.calculate_logic exception: %s", exc)
            return 0.0

    def validate_logic(self, formula: str) -> Dict[str, Any]:
        """Validate formula syntax and basic operator sequences."""
        try:
            if any(seq in formula for seq in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}

            test_formula = formula
            vars_found = re.findall(r"\{(\w+)\}", formula)
            for var in vars_found:
                test_formula = test_formula.replace(f"{{{var}}}", "1")

            # Ensure the expression parses as a Python expression
            ast.parse(test_formula, mode="eval")
            return {"is_valid": True, "error": None}
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return {"is_valid": False, "error": str(exc)}


class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation."""

    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        """Define a named formula."""
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        """Alias for define."""
        self.define(name, formula)

    def calculate(self, formula_or_name: str, variables: Optional[Dict[str, Any]] = None) -> float:
        """Calculate a formula given either a raw formula or a previously defined name."""
        variables = variables or {}
        formula = self.formulas.get(formula_or_name, formula_or_name)
        try:
            return float(self.core.calculate_logic(formula, variables))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.error("Formula calculation failed: %s", exc)
            return 0.0

    def validate(self, formula: str) -> FormulaValidation:
        """Return structured validation result for a formula."""
        result = self.core.validate_logic(formula)
        return FormulaValidation(is_valid=result["is_valid"], error=result["error"])

    def validate_formula(self, formula: str) -> bool:
        """Convenience boolean validation check."""
        return self.validate(formula).is_valid
