# Copyright 2026 PyAgent Authors
# MathAgent: Specialized Mathematical Reasoning Agent - Phase 319 Enhanced

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import math
import re
from typing import Any, Dict, List, Optional, Union
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION

# Safe math namespace for expression evaluation
SAFE_MATH_NAMESPACE = {
    "__builtins__": {},
    "abs": abs, "round": round, "min": min, "max": max, "sum": sum, "len": len,
    "pow": pow, "int": int, "float": float,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "log": math.log, "log10": math.log10, "log2": math.log2, "exp": math.exp,
    "sqrt": math.sqrt, "ceil": math.ceil, "floor": math.floor,
    "factorial": math.factorial, "gcd": math.gcd,
    "pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf,
    "degrees": math.degrees, "radians": math.radians,
}

class MathAgent(BaseAgent):
    """
    Agent specializing in symbolic math, numerical computation, and logical proofs.
    Utilizes Rust-accelerated evaluation where available.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Math Agent. You solve complex mathematical problems, "
            "perform symbolic manipulations, and verify logical proofs. "
            "Always prefer precise numerical outputs and structured reasoning. "
            "Show your work step-by-step."
        )
        self._calculation_history: List[Dict[str, Any]] = []

    @as_tool
    async def solve_expression(self, expression: str) -> Dict[str, Any]:
        """Evaluates a mathematical expression safely."""
        # Sanitize input
        sanitized = self._sanitize_expression(expression)
        
        try:
            # Try Rust-accelerated evaluation first
            try:
                import rust_core
                if hasattr(rust_core, "evaluate_formula"):
                    result = rust_core.evaluate_formula(sanitized)
                    self._record_calculation(expression, result, "rust")
                    return {"expression": expression, "result": result, "status": "success", "engine": "rust"}
            except (ImportError, AttributeError):
                pass
            
            # Python safe eval fallback
            result = eval(sanitized, SAFE_MATH_NAMESPACE)
            self._record_calculation(expression, result, "python")
            return {"expression": expression, "result": result, "status": "success", "engine": "python"}
            
        except Exception as e:
            logging.debug(f"MathAgent: Direct evaluation failed: {e}")
            # Fallback to LLM reasoning for complex/symbolic math
            return await self._llm_solve(expression)

    @as_tool
    async def solve_equation(self, equation: str, variable: str = "x") -> Dict[str, Any]:
        """Solves algebraic equations for a variable."""
        prompt = (
            f"Solve the equation: {equation}\n"
            f"Solve for: {variable}\n"
            "Show step-by-step solution and provide the final answer in the format: {variable} = value"
        )
        result = await self.improve_content(prompt)
        
        # Try to extract numerical answer
        match = re.search(rf"{variable}\s*=\s*([-\d.]+)", result)
        extracted = float(match.group(1)) if match else None
        
        return {
            "equation": equation,
            "variable": variable,
            "solution": extracted,
            "reasoning": result,
            "status": "success" if extracted else "symbolic"
        }

    @as_tool
    async def compute_derivative(self, expression: str, variable: str = "x") -> Dict[str, Any]:
        """Computes the derivative of an expression."""
        prompt = f"Compute the derivative of f({variable}) = {expression} with respect to {variable}. Show your work."
        result = await self.improve_content(prompt)
        return {"expression": expression, "variable": variable, "derivative": result}

    @as_tool
    async def compute_integral(self, expression: str, variable: str = "x", bounds: Optional[tuple] = None) -> Dict[str, Any]:
        """Computes the integral (definite or indefinite)."""
        if bounds:
            prompt = f"Compute the definite integral of {expression} d{variable} from {bounds[0]} to {bounds[1]}."
        else:
            prompt = f"Compute the indefinite integral of {expression} d{variable}."
        result = await self.improve_content(prompt)
        return {"expression": expression, "variable": variable, "bounds": bounds, "integral": result}

    @as_tool
    async def prove_statement(self, statement: str, method: str = "direct") -> Dict[str, Any]:
        """Attempts to prove a mathematical statement."""
        prompt = (
            f"Prove the following statement using {method} proof:\n"
            f"Statement: {statement}\n"
            "Provide a rigorous proof with clear logical steps."
        )
        proof = await self.improve_content(prompt)
        return {"statement": statement, "method": method, "proof": proof}

    @as_tool
    async def matrix_operation(self, operation: str, matrices: List[List[List[float]]]) -> Dict[str, Any]:
        """Performs matrix operations (multiply, add, determinant, inverse, etc.)."""
        try:
            import numpy as np
            
            if operation == "multiply" and len(matrices) >= 2:
                result = np.array(matrices[0])
                for m in matrices[1:]:
                    result = np.dot(result, np.array(m))
                return {"operation": operation, "result": result.tolist(), "status": "success"}
            elif operation == "determinant" and matrices:
                det = np.linalg.det(np.array(matrices[0]))
                return {"operation": operation, "result": det, "status": "success"}
            elif operation == "inverse" and matrices:
                inv = np.linalg.inv(np.array(matrices[0]))
                return {"operation": operation, "result": inv.tolist(), "status": "success"}
            elif operation == "eigenvalues" and matrices:
                eigenvalues = np.linalg.eigvals(np.array(matrices[0]))
                return {"operation": operation, "result": eigenvalues.tolist(), "status": "success"}
        except Exception as e:
            return {"operation": operation, "error": str(e), "status": "failed"}
        
        return {"operation": operation, "status": "unsupported"}

    def _sanitize_expression(self, expr: str) -> str:
        """Removes potentially dangerous constructs."""
        # Remove anything that looks like function calls to non-math functions
        sanitized = re.sub(r'\b(import|exec|eval|compile|open|__\w+__)\b', '', expr)
        return sanitized.strip()

    def _record_calculation(self, expression: str, result: Any, engine: str) -> None:
        import time
        self._calculation_history.append({
            "expression": expression,
            "result": result,
            "engine": engine,
            "timestamp": time.time()
        })

    async def _llm_solve(self, expression: str) -> Dict[str, Any]:
        """Uses LLM for complex mathematical reasoning."""
        prompt = f"Solve this math problem step-by-step: {expression}\nProvide the final numerical answer if possible."
        llm_result = await self.improve_content(prompt)
        
        # Try to extract a number from the response
        numbers = re.findall(r'[-+]?\d*\.?\d+', llm_result)
        final_answer = float(numbers[-1]) if numbers else None
        
        return {
            "expression": expression,
            "result": final_answer,
            "reasoning": llm_result,
            "status": "llm_fallback",
            "engine": "llm"
        }
