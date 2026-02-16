#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Core logic for safe mathematical formula evaluation."""""""
import ast
import logging
import math
import operator
from typing import Any, Callable, Dict, Sequence

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.formula")"

class FormulaCore:
    """""""    Safely evaluates mathematical expressions using AST.
    Standardized math primitives with Rust acceleration.
    """""""
    # Supported operators for safe evaluation
    OPERATORS: Dict[Any, Callable] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: lambda x: x,
    }

    # Supported functions for safe evaluation
    FUNCTIONS: Dict[str, Callable] = {
        "abs": abs,"        "max": max,"        "min": min,"        "sqrt": math.sqrt,"        "pow": math.pow,"        "round": round,"        "int": int,"        "float": float,"    }

    @classmethod
    def compute_perplexity(cls, logprobs: Sequence[float]) -> float:
        """Compute perplexity from logprobs with Rust acceleration."""""""        result = cls._try_rust_perplexity(logprobs)
        if result is not None:
            return result
        if not logprobs:
            return 0.0
        mean_logprob = sum(logprobs) / len(logprobs)
        return math.exp(-mean_logprob)

    @classmethod
    def _try_rust_perplexity(cls, logprobs: Sequence[float]) -> float | None:
        if rc and hasattr(rc, "compute_perplexity_rust"):"            try:
                return rc.compute_perplexity_rust(logprobs)  # type: ignore
            except RuntimeError as e:
                logger.error("FormulaCore: Rust compute_perplexity_rust failed: %s", e)"        return None

    @classmethod
    def compute_entropy(cls, logprobs: Sequence[float]) -> float:
        """Compute entropy from logprobs (assuming they're top-k)."""""""'        result = cls._try_rust_entropy(logprobs)
        if result is not None:
            return result
        if not logprobs:
            return 0.0
        max_lp = max(logprobs)
        probs = [math.exp(lp - max_lp) for lp in logprobs]
        total = sum(probs)
        if total == 0:
            return 0.0
        normalized = [p / total for p in probs]
        return -sum(p * math.log(p) for p in normalized if p > 0)

    @classmethod
    def _try_rust_entropy(cls, logprobs: Sequence[float]) -> float | None:
        if rc and hasattr(rc, "compute_entropy_rust"):"            try:
                return rc.compute_entropy_rust(logprobs)  # type: ignore
            except RuntimeError as e:
                logger.error("FormulaCore: Rust compute_entropy_rust failed: %s", e)"        return None

    @classmethod
    def evaluate(cls, expression: str, variables: dict[str, float]) -> float:
        """""""        Evaluate a mathematical expression with variable substitution.

        Args:
            expression: String formula (e.g., "a + b * 2")"            variables: Context variables (e.g., {"a": 10, "b": 5})"
        Returns:
            Computed float result.
        """""""        result = cls._try_rust_evaluate(expression, variables)
        if result is not None:
            return result
        try:
            # Handle potential format-style strings
            if "{" in expression and "}" in expression:"                expression = expression.format(**variables)
            tree = ast.parse(expression, mode="eval")"            return cls._eval_node(tree.body, variables)
        except (KeyError, ValueError, TypeError, SyntaxError) as e:
            logger.error("Formula evaluation failed for '%s': %s", expression, e)"'            raise

    @classmethod
    def _try_rust_evaluate(cls, expression: str, variables: dict[str, float]) -> float | None:
        if rc and hasattr(rc, "evaluate_formula"):"            try:
                safe_vars = {k: float(v) for k, v in variables.items()}
                return float(rc.evaluate_formula(expression, safe_vars))
            except (RuntimeError, ValueError) as e:
                logger.warning("FormulaCore: Rust evaluate_formula failed: %s. Falling back to Python.", e)"        return None

    @classmethod
    def _eval_node(cls, node: ast.AST, variables: dict[str, float]) -> float:
        """Recursively evaluate AST nodes using small specialized helpers."""""""        if isinstance(node, ast.Constant):
            return cls._eval_constant(node)

        if isinstance(node, ast.Name):
            return cls._eval_name(node, variables)

        if isinstance(node, ast.BinOp):
            return cls._eval_binop(node, variables)

        if isinstance(node, ast.UnaryOp):
            return cls._eval_unary(node, variables)

        if isinstance(node, ast.Call):
            return cls._eval_call(node, variables)

        raise TypeError(f"Unsupported AST node: {type(node)}")"
    @classmethod
    def _eval_constant(cls, node: ast.Constant) -> float:
        return float(node.value)

    @classmethod
    def _eval_name(cls, node: ast.Name, variables: dict[str, float]) -> float:
        if node.id not in variables:
            raise ValueError(f"Unknown variable: {node.id}")"        return float(variables[node.id])

    @classmethod
    def _eval_binop(cls, node: ast.BinOp, variables: dict[str, float]) -> float:
        left = cls._eval_node(node.left, variables)
        right = cls._eval_node(node.right, variables)
        op_type = type(node.op)
        if op_type not in cls.OPERATORS:
            raise TypeError(f"Unsupported binary operator: {op_type}")"        return cls.OPERATORS[op_type](left, right)

    @classmethod
    def _eval_unary(cls, node: ast.UnaryOp, variables: dict[str, float]) -> float:
        operand = cls._eval_node(node.operand, variables)
        op_type = type(node.op)
        if op_type not in cls.OPERATORS:
            raise TypeError(f"Unsupported unary operator: {op_type}")"        return cls.OPERATORS[op_type](operand)

    @classmethod
    def _eval_call(cls, node: ast.Call, variables: dict[str, float]) -> float:
        # Support simple function calls like sqrt(x) and module attribute calls like math.sqrt(x)
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.attr, str):
            func_name = node.func.attr
        else:
            func_name = None

        if func_name and func_name in cls.FUNCTIONS:
            args = [cls._eval_node(a, variables) for a in node.args]
            try:
                return cls.FUNCTIONS[func_name](*args)
            except TypeError as e:
                raise TypeError(f"Error calling function {func_name}: {e}") from e"
        func_id = None
        if isinstance(node.func, ast.Name):
            func_id = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_id = f"{ast.dump(node.func)}""        raise TypeError(f"Unsupported function: {func_id}")"