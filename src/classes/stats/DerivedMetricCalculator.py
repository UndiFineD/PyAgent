#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .DerivedMetric import DerivedMetric

from typing import Dict, List, Optional
import ast
import operator
import logging
import math

class DerivedMetricCalculator:
    """Calculate derived metrics from dependencies using safe AST evaluation."""

    def __init__(self) -> None:
        """Initialize derived metric calculator."""
        self.derived_metrics: Dict[str, DerivedMetric] = {}
        self._cache: Dict[str, float] = {}
        # Safe operator mapping
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

    def _eval_node(self, node: ast.AST) -> float:
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Constant):
            return float(node.value)
        elif isinstance(node, ast.Num):
            return float(node.n)
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                args = [self._eval_node(a) for a in node.args]
                if func_name == "abs": return abs(args[0])
                if func_name == "max": return max(args)
                if func_name == "min": return min(args)
                if func_name == "sqrt": return math.sqrt(args[0])
                if func_name == "pow": return math.pow(args[0], args[1])
            raise TypeError(f"Unsupported function: {node.func}")
        else:
            raise TypeError(f"Unsupported operation in formula: {type(node)}")

    def register_derived(
        self,
        name: str,
        dependencies: List[str],
        formula: str,
        description: str = ""
    ) -> DerivedMetric:
        """Register a derived metric.

        Args:
            name: Name for the derived metric.
            dependencies: List of metric names this depends on.
            formula: Formula string using {metric_name} placeholders.
            description: Description of the metric.

        Returns:
            The registered derived metric.
        """
        derived = DerivedMetric(
            name=name,
            dependencies=dependencies,
            formula=formula,
            description=description
        )
        self.derived_metrics[name] = derived
        return derived

    def calculate(
        self,
        name: str,
        metric_values: Dict[str, float]
    ) -> Optional[float]:
        """Calculate a derived metric value.

        Args:
            name: The derived metric name.
            metric_values: Current values of all metrics.

        Returns:
            Calculated value or None if missing dependencies.
        """
        derived = self.derived_metrics.get(name)
        if not derived:
            return None

        # Check all dependencies are available
        for dep in derived.dependencies:
            if dep not in metric_values:
                return None

        # Replace placeholders and evaluate
        formula = derived.formula
        for dep in derived.dependencies:
            formula = formula.replace(f"{{{dep}}}", str(metric_values[dep]))

        try:
            # Basic validation (clean placeholder injection still matters)
            dangerous_keywords = ["import", "open", "os.", "subprocess", "sys.", "eval", "exec", "__"]
            if any(kw in formula for kw in dangerous_keywords):
                logging.error(f"Blocked potentially dangerous formula: {formula}")
                return None

            # Safe AST evaluation
            tree = ast.parse(formula, mode='eval')
            result = self._eval_node(tree.body)
            
            self._cache[name] = result
            return result
        except Exception as e:
            logging.error(f"Failed to calculate {name}: {e}")
            return None

    def get_all_derived(
        self,
        metric_values: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate all derived metrics.

        Args:
            metric_values: Current values of all metrics.

        Returns:
            Dictionary of all calculated derived metrics.
        """
        results: Dict[str, float] = {}
        for name in self.derived_metrics:
            value = self.calculate(name, metric_values)
            if value is not None:
                results[name] = value
        return results
