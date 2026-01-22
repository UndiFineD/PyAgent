#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

"""
Formula processing and calculation engine.
(Facade for src.core.base.common.formula_core)
"""

from __future__ import annotations
import ast
import re
import logging
import contextlib
from typing import Any, Dict, Optional
from dataclasses import dataclass

from src.core.base.common.formula_core import FormulaCore

try:
    import rust_core as rc
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
        """Core logic for calculating a formula result with support for aggregates."""
        # Check Rust acceleration first
        if rc and "AVG(" not in formula:
            with contextlib.suppress(Exception):
                float_vars = {
                    k: float(v)
                    for k, v in variables.items()
                    if isinstance(v, (int, float))
                }
                # Support both naming conventions
                if hasattr(rc, "evaluate_formula"):
                    return rc.evaluate_formula(formula, float_vars)
                elif hasattr(rc, "evaluate_formula_rust"):
                    return rc.evaluate_formula_rust(formula, float_vars)

        # Handle simple AVG aggregate manually
        if "AVG(" in formula:
            match = re.search(r"AVG\(\{(\w+)\}\)", formula)
            if match:
                var_name = match.group(1)
                if var_name in variables:
                    values = variables[var_name]
                    if isinstance(values, list) and values:
                        return sum(values) / len(values)
            return 0.0

        try:
            # Substitute variables in format {var_name}
            eval_formula = formula
            substituted_vars = {}
            for var_name, var_value in variables.items():
                if f"{{{var_name}}}" in eval_formula:
                    # If it's a simple substitution, we can do it via string or dict
                    substituted_vars[var_name] = float(var_value)
            
            # Use base class evaluate if possible
            return self.evaluate(formula.replace("{", "").replace("}", ""), substituted_vars)
        except Exception:
            return 0.0

    def validate_logic(self, formula: str) -> Dict[str, Any]:
        """Core logic for validating formula syntax."""
        try:
            if any(seq in formula for seq in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}

            test_formula = formula
            vars_found: list[str] = re.findall(r"\{(\w+)\}", formula)
            for var in vars_found:
                test_formula = test_formula.replace(f"{{{var}}}", "1")

            ast.parse(test_formula, mode="eval")
            return {"is_valid": True, "error": None}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}

class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation."""

    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        self.define(name, formula)

    def calculate(
        self, formula_or_name: str, variables: Dict[str, Any] | None = None
    ) -> float:
        variables = variables or {}
        formula = self.formulas.get(formula_or_name, formula_or_name)
        try:
            return self.core.calculate_logic(formula, variables)
        except Exception as e:
            logging.error(f"Formula calculation failed: {e}")
            return 0.0

    def validate(self, formula: str) -> FormulaValidation:
        result = self.core.validate_logic(formula)
        return FormulaValidation(is_valid=result["is_valid"], error=result["error"])

    def validate_formula(self, formula: str) -> bool:
        return self.validate(formula).is_valid
