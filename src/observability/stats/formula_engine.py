#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Formula processing and calculation engine.

from __future__ import annotations
import ast
import logging
import operator
import re
from typing import Any
from dataclasses import dataclass

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)




@dataclass





class FormulaValidation:
    """Result of formula validation."""
    is_valid: bool = True
    error: str = ""



class FormulaEngineCore:
    """Pure logic core for formula calculations."""

    def __init__(self) -> None:
        self.operators: dict[type[ast.AST], Any] = {
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
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate_logic(self, formula: str, variables: dict[str, Any]) -> float:
        """Core logic for calculating a formula result."""
        if rc and "AVG(" not in formula:
            try:
                float_vars = {k: float(v) for k, v in variables.items() if isinstance(v, (int, float))}
                return rc.evaluate_formula(formula, float_vars)  # type: ignore[attr-defined]
            except Exception:
                pass

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
            eval_formula = formula
            for var_name, var_value in variables.items():
                eval_formula = eval_formula.replace(f"{{{var_name}}}", str(var_value))
            tree = ast.parse(eval_formula, mode='eval')







            return self._eval_node(tree.body)
        except Exception:
            return 0.0

    def validate_logic(self, formula: str) -> dict[str, Any]:
        """Core logic for validating formula syntax."""
        try:
            if any(seq in formula for seq in ["+++", "***", "---"]):
                return {"is_valid": False, "error": "Invalid operator sequence"}




            test_formula = formula
            vars_found: list[str] = re.findall(r'\{(\w+)\}', formula)
            for var in vars_found:
                test_formula = test_formula.replace(f"{{{var}}}", "1")

            ast.parse(test_formula, mode='eval')
            return {"is_valid": True, "error": None}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}





class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation."""
    def __init__(self) -> None:
        self.formulas: dict[str, str] = {}
        self.core = FormulaEngineCore()

    def define(self, name: str, formula: str) -> None:
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        self.define(name, formula)

    def calculate(self, formula_or_name: str, variables: dict[str, Any] | None = None) -> float:
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
