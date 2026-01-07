#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Test generation and case minimization."""

import ast
from typing import Any, Callable, List, Tuple

from .models import GeneratedTest


class TestGenerator:
    """Generate tests from specifications."""
    __test__ = False

    def __init__(self) -> None:
        """Initialize test generator."""
        self.generated: List[GeneratedTest] = []
        self._templates: dict[str, str] = {}

    def add_template(self, name: str, template: str) -> None:
        """Add a test template."""
        self._templates[name] = template

    def generate_from_spec(
        self,
        specification: str,
        function_name: str,
        input_type: str = "Any",
        output_type: str = "Any"
    ) -> GeneratedTest:
        """Generate test from specification."""
        test_name = f"test_{function_name}_{len(self.generated)}"

        code = (
            f"def {test_name}():\n"
            f"    \"\"\"{specification}\"\"\"\n"
            f"    # TODO: Implement test for {function_name}\n"
            f"    # Input type: {input_type}\n"
            f"    # Output type: {output_type}\n"
            f"    pass\n"
        )

        generated = GeneratedTest(
            name=test_name,
            specification=specification,
            generated_code=code,
            confidence=0.6
        )
        self.generated.append(generated)
        return generated

    def generate_parametrized(
        self,
        function_name: str,
        test_cases: List[Tuple[Any, Any]]
    ) -> GeneratedTest:
        """Generate parametrized test."""
        test_name = f"test_{function_name}_parametrized"
        params = ", ".join(str(tc) for tc in test_cases)
        code = (
            f"@pytest.mark.parametrize('input_val,expected', [\n"
            f"    {params}\n"
            f"])\n"
            f"def {test_name}(input_val, expected):\n"
            f"    result={function_name}(input_val)\n"
            f"    assert result == expected\n"
        )
        generated = GeneratedTest(
            name=test_name,
            specification=f"Parametrized test for {function_name}",
            generated_code=code,
            confidence=0.8
        )
        self.generated.append(generated)
        return generated

    def validate_generated(self, test_id: int) -> bool:
        """Validate a generated test has valid syntax."""
        if test_id < 0 or test_id >= len(self.generated):
            return False
        try:
            ast.parse(self.generated[test_id].generated_code)
            self.generated[test_id].validated = True
            return True
        except SyntaxError:
            return False

    def export_all(self) -> str:
        """Export all generated tests."""
        validated = [g for g in self.generated if g.validated]
        return "\n\n".join(g.generated_code for g in validated)


class TestCaseMinimizer:
    """Minimize test cases for debugging."""
    __test__ = False

    def __init__(self) -> None:
        """Initialize test case minimizer."""
        self.history: List[dict[str, Any]] = []

    def minimize_string(
        self,
        input_str: str,
        test_fn: Callable[[str], bool]
    ) -> str:
        """Minimize a string input using delta debugging."""
        current = input_str
        while len(current) > 1:
            mid = len(current) // 2
            left = current[:mid]
            right = current[mid:]
            if test_fn(left):
                current = left
            elif test_fn(right):
                current = right
            else:
                break
        
        reduction = 1 - len(current) / len(input_str) if input_str else 0
        self.history.append({
            "original": input_str,
            "minimized": current,
            "reduction": reduction
        })
        return current

    def minimize_list(
        self,
        input_list: List[Any],
        test_fn: Callable[[List[Any]], bool]
    ) -> List[Any]:
        """Minimize a list input by removing elements."""
        current = input_list.copy()
        i = 0
        while i < len(current):
            candidate = current[:i] + current[i + 1:]
            if test_fn(candidate):
                current = candidate
            else:
                i += 1
        
        self.history.append({
            "original_length": len(input_list),
            "minimized_length": len(current)
        })
        return current

    def get_minimization_stats(self) -> dict[str, Any]:
        """Get minimization statistics."""
        if not self.history:
            return {"total": 0}
        
        reductions = [h.get("reduction", 0) for h in self.history if "reduction" in h]
        avg_reduction = sum(reductions) / len(reductions) if reductions else 0
        
        return {
            "total_minimizations": len(self.history),
            "average_reduction": avg_reduction,
            "total": len(self.history)
        }

    def minimize_string(
        self,
        input_str: str,
        test_fn: Callable[[str], bool]
    ) -> str:
        """Minimize a string input."""
        current = input_str

        while len(current) > 1:
            mid = len(current) // 2
            left = current[:mid]
            right = current[mid:]
            if test_fn(left):
                current = left
            elif test_fn(right):
                current = right
            else:
                break
        self.history.append({
            "original": input_str,
            "minimized": current,
            "reduction": 1 - len(current) / len(input_str)
        })
        return current

    def minimize_list(
        self,
        input_list: List[Any],
        test_fn: Callable[[List[Any]], bool]
    ) -> List[Any]:
        """Minimize a list input."""
        current = input_list.copy()

        i = 0
        while i < len(current):
            candidate = current[:i] + current[i + 1:]
            if test_fn(candidate):
                current = candidate
            else:
                i += 1
        self.history.append({
            "original_length": len(input_list),
            "minimized_length": len(current)
        })
        return current

    def get_minimization_stats(self) -> dict[str, Any]:
        """Get minimization statistics."""
        if not self.history:
            return {"total": 0}
        reductions = [h.get("reduction", 0) for h in self.history if "reduction" in h]
        avg_reduction = sum(reductions) / len(reductions) if reductions else 0
        return {
            "total_minimizations": len(self.history),
            "average_reduction": avg_reduction
        }


class TestDocGenerator:
    """Generates documentation from tests."""
    __test__ = False

    def __init__(self) -> None:
        """Initialize doc generator."""
        self.tests: List[dict[str, Any]] = []

    def add_test(self, name: str, module: str = "unknown", docstring: str = "", code: str = "") -> None:
        """Add test for documentation."""
        self.tests.append({"name": name, "module": module, "docstring": docstring, "code": code})

    def generate(self) -> str:
        """Generate a human-readable documentation summary."""
        parts: List[str] = []
        for test in self.tests:
            title = test.get("name", "")
            doc = test.get("docstring", "")
            code = test.get("code", "")
            parts.append(f"{title}: {doc}\n{code}".strip())
        return "\n\n".join(parts)

    def generate_grouped(self) -> dict[str, List[dict[str, Any]]]:
        """Generate documentation grouped by module."""
        return self.group_by_module(self.tests)

    def extract_examples(self, test_code: str) -> List[dict[str, str]]:
        """Extract examples from test code."""
        return [{"example": test_code}] if test_code else []

    def group_by_module(self, tests: List[dict[str, Any]]) -> dict[str, List[dict[str, Any]]]:
        """Group tests by module."""
        result: dict[str, List[dict[str, Any]]] = {}
        for test in tests:
            module = test.get("module", "unknown")
            if module not in result:
                result[module] = []
            result[module].append(test)
        return result
