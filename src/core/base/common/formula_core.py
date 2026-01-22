<<<<<<< HEAD
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Core logic for safe mathematical formula evaluation."""

import ast
import logging
import math
import operator
from typing import Any, Callable, Dict, Sequence
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Core logic for safe mathematical formula evaluation."""

import ast
import math
import operator
import logging
from typing import Dict, Any, Callable, Sequence
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
<<<<<<< HEAD
    rc = None

logger = logging.getLogger("pyagent.formula")


=======
    rc = None  # type: ignore[assignment]

logger = logging.getLogger("pyagent.formula")

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class FormulaCore:
    """
    Safely evaluates mathematical expressions using AST.
    Standardized math primitives with Rust acceleration.
    """
<<<<<<< HEAD

=======
    
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
        "abs": abs,
        "max": max,
        "min": min,
        "sqrt": math.sqrt,
        "pow": math.pow,
        "round": round,
        "int": int,
        "float": float,
    }

    @classmethod
    def compute_perplexity(cls, logprobs: Sequence[float]) -> float:
        """Compute perplexity from logprobs with Rust acceleration."""
<<<<<<< HEAD
        if rc and hasattr(rc, "compute_perplexity_rust"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.compute_perplexity_rust(logprobs)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
        if rc and hasattr(rc, "compute_perplexity_rust"):
            return rc.compute_perplexity_rust(logprobs)
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if not logprobs:
            return 0.0
        mean_logprob = sum(logprobs) / len(logprobs)
        return math.exp(-mean_logprob)

    @classmethod
    def compute_entropy(cls, logprobs: Sequence[float]) -> float:
        """Compute entropy from logprobs (assuming they're top-k)."""
<<<<<<< HEAD
        if rc and hasattr(rc, "compute_entropy_rust"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.compute_entropy_rust(logprobs)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass
=======
        if rc and hasattr(rc, "compute_entropy_rust"):
            return rc.compute_entropy_rust(logprobs)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

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
    def evaluate(cls, expression: str, variables: Dict[str, float]) -> float:
        """
        Evaluate a mathematical expression with variable substitution.
<<<<<<< HEAD

        Args:
            expression: String formula (e.g., "a + b * 2")
            variables: Context variables (e.g., {"a": 10, "b": 5})

        Returns:
            Computed float result.
        """
        # Phase 40: Rust Acceleration
        if rc and hasattr(rc, "evaluate_formula"):
            try:
                # Type cast variables to ensure f64 compatibility
                safe_vars = {k: float(v) for k, v in variables.items()}
                return float(rc.evaluate_formula(expression, safe_vars))
            except Exception as e:
                # Fallback to Python if Rust fails or panic occurs
                logger.debug("Rust formula evaluation failed (used fallback): %s", e)

=======
        
        Args:
            expression: String formula (e.g., "a + b * 2")
            variables: Context variables (e.g., {"a": 10, "b": 5})
            
        Returns:
            Computed float result.
        """
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        try:
            # Handle potential format-style strings
            if "{" in expression and "}" in expression:
                expression = expression.format(**variables)
<<<<<<< HEAD

            tree = ast.parse(expression, mode="eval")
            return cls._eval_node(tree.body, variables)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
=======
                
            tree = ast.parse(expression, mode="eval")
            return cls._eval_node(tree.body, variables)
        except Exception as e:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            logger.error("Formula evaluation failed for '%s': %s", expression, e)
            raise

    @classmethod
    def _eval_node(cls, node: ast.AST, variables: Dict[str, float]) -> float:
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):
            return float(node.value)
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if isinstance(node, ast.Name):
            if node.id not in variables:
                raise ValueError(f"Unknown variable: {node.id}")
            return float(variables[node.id])
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left, variables)
            right = cls._eval_node(node.right, variables)
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise TypeError(f"Unsupported binary operator: {op_type}")
            return cls.OPERATORS[op_type](left, right)
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand, variables)
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise TypeError(f"Unsupported unary operator: {op_type}")
            return cls.OPERATORS[op_type](operand)

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in cls.FUNCTIONS:
                    args = [cls._eval_node(a, variables) for a in node.args]
                    return cls.FUNCTIONS[func_name](*args)
<<<<<<< HEAD
            func_id = node.func.id if isinstance(node.func, ast.Name) else node.func
            raise TypeError(f"Unsupported function: {func_id}")
=======
            raise TypeError(f"Unsupported function: {node.func if not isinstance(node.func, ast.Name) else node.func.id}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        raise TypeError(f"Unsupported AST node: {type(node)}")
