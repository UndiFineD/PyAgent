#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .FormulaValidation import FormulaValidation

from typing import Any, Dict, List, Optional

import ast
import operator
import logging

class FormulaEngine:
    """Processes metric formulas and calculations using safe AST evaluation."""
    def __init__(self) -> None:
        self.formulas: Dict[str, str] = {}
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

    def define(self, name: str, formula: str) -> None:
        """Define a formula."""
        self.formulas[name] = formula

    def define_formula(self, name: str, formula: str) -> None:
        """Define a formula (backward compat)."""
        self.define(name, formula)

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return float(node.value)
        elif isinstance(node, ast.Num):  # Python < 3.8
            return float(node.n)
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate(self, formula_or_name: str, variables: Optional[Dict[str, Any]] = None) -> float:
        """Calculate formula result."""
        variables = variables or {}
        # If formula_or_name is in formulas dict, use stored formula
        if formula_or_name in self.formulas:
            formula = self.formulas[formula_or_name]
        else:
            formula = formula_or_name
            
        # Handle special functions like AVG
        if "AVG(" in formula:
            import re
            match = re.search(r'AVG\(\{(\w+)\}\)', formula)
            if match:
                var_name = match.group(1)
                if var_name in variables:
                    values: List[float] = variables[var_name]
                    if values:
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
        except Exception as e:
            logging.error(f"Formula calculation failed: {e}")
            return 0.0


    def validate(self, formula: str) -> FormulaValidation:
        """Validate formula syntax."""
        try:
            # Basic validation - check for invalid operators
            if "+++" in formula or "***" in formula or "---" in formula:
                return FormulaValidation(is_valid=False, error="Invalid operator sequence")

            # Handle template formulas with variables
            if "{" in formula and "}" in formula:
                test_formula = formula
                import re
                # Find all variable names and replace them
                vars_found = re.findall(r'\{(\w+)\}', formula)
                for var in vars_found:
                    test_formula = test_formula.replace(f"{{{var}}}", "1")

                # Try to compile the test formula
                compile(test_formula, '<string>', 'eval')
            else:
                # Direct formula validation
                compile(formula, '<string>', 'eval')

            return FormulaValidation(is_valid=True)
        except (SyntaxError, ValueError) as e:
            return FormulaValidation(is_valid=False, error=str(e))

    def validate_formula(self, formula: str) -> bool:
        """Validate formula syntax (backward compat)."""
        return self.validate(formula).is_valid
