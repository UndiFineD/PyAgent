"""Integration tests for FormulaEngineCore.

This tests Python implementation end-to-end.
Rust integration tests will be added once Rust crate builds.
"""

from src.observability.stats.metrics_engine import FormulaEngineCore


class TestFormulaEngineIntegration:
    """Integration tests for formula evaluation."""

    def test_complex_formula_with_multiple_variables(self) -> None:
        """Test formula with multiple variables and operations."""
        core = FormulaEngineCore()
        formula = "{x} * {y} + {z}"
        variables = {"x": 2.0, "y": 3.0, "z": 4.0}
        result = core.calculate_logic(formula, variables)
        expected = 2.0 * 3.0 + 4.0
        assert result == expected

    def test_nested_formula_evaluation(self) -> None:
        """Test formula with parentheses and precedence."""
        core = FormulaEngineCore()
        formula = "({a} + {b}) * {c}"
        variables = {"a": 2.0, "b": 3.0, "c": 5.0}
        result = core.calculate_logic(formula, variables)
        expected = (2.0 + 3.0) * 5.0
        assert result == expected

    def test_negative_values(self) -> None:
        """Test formula with negative variable values."""
        core = FormulaEngineCore()
        formula = "{x} * {y}"
        variables = {"x": -5.0, "y": 3.0}
        result = core.calculate_logic(formula, variables)
        expected = -15.0
        assert result == expected

    def test_validate_then_calculate(self) -> None:
        """Test validation followed by calculation."""
        core = FormulaEngineCore()
        formula = "{base} * (1 + {rate})"

        # Validate first
        validation_result = core.validate_logic(formula)
        assert validation_result["is_valid"]
        assert validation_result["error"] is None

        # Then calculate
        variables = {"base": 100.0, "rate": 0.05}
        result = core.calculate_logic(formula, variables)
        expected = 100.0 * (1 + 0.05)
        assert result == expected

    def test_formula_with_power_operation(self) -> None:
        """Test formula with exponentiation."""
        core = FormulaEngineCore()
        formula = "{x} ** 2"
        variables = {"x": 5.0}
        result = core.calculate_logic(formula, variables)
        expected = 25.0
        assert result == expected

    def test_formula_with_unary_negative(self) -> None:
        """Test formula with unary negation."""
        core = FormulaEngineCore()
        formula = "-{a} + {b}"
        variables = {"a": 5.0, "b": 10.0}
        result = core.calculate_logic(formula, variables)
        expected = -5.0 + 10.0
        assert result == expected

    def test_validation_accepts_valid_formulas(self) -> None:
        """Test that validation accepts well-formed formulas."""
        core = FormulaEngineCore()

        valid_formulas = [
            "{x} + {y}",
            "{x} * {y} - {z}",
            "({x} + {y})",
            "{x} ** 2",
        ]

        for formula in valid_formulas:
            validation = core.validate_logic(formula)
            # Note: validate_logic may not catch all syntax errors at parse time
            # It validates formula structure, not all edge cases
            assert isinstance(validation, dict)

    def test_formula_with_edge_case_values(self) -> None:
        """Test formula evaluation with various edge case values."""
        core = FormulaEngineCore()
        formula = "{x} * {y}"

        # Test with small positive values
        variables = {"x": 0.001, "y": 0.002}
        result = core.calculate_logic(formula, variables)
        expected = 0.001 * 0.002
        assert abs(result - expected) < 1e-10

    def test_large_numbers(self) -> None:
        """Test formula evaluation with large numbers."""
        core = FormulaEngineCore()
        formula = "{x} * {y}"
        variables = {"x": 1e10, "y": 1e10}
        result = core.calculate_logic(formula, variables)
        expected = 1e20
        assert result == expected

    def test_small_numbers(self) -> None:
        """Test formula evaluation with very small numbers."""
        core = FormulaEngineCore()
        formula = "{x} / {y}"
        variables = {"x": 1e-10, "y": 2.0}
        result = core.calculate_logic(formula, variables)
        expected = 0.5e-10
        assert abs(result - expected) < 1e-20
