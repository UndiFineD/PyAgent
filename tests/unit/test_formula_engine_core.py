import math

from hypothesis import given, strategies as st

from src.observability.stats.Metrics_engine import FormulaEngineCore


@given(
    a=st.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False),
    b=st.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False),
    op=st.sampled_from(["+", "-", "*"]),
)
def test_calculate_logic_basic_ops(a: float, b: float, op: str) -> None:
    core = FormulaEngineCore()

    formula = f"{{a}}{op}{{b}}"
    variables = {"a": a, "b": b}

    result = core.calculate_logic(formula, variables)

    expected = {
        "+": a + b,
        "-": a - b,
        "*": a * b,
    }[op]

    assert math.isfinite(result)
    assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-9)


@given(
    values=st.lists(
        st.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=10,
    )
)
def test_calculate_logic_avg(values: list[float]) -> None:
    core = FormulaEngineCore()
    result = core.calculate_logic("AVG({values})", {"values": values})
    expected = sum(values) / len(values)
    assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-9)


def test_validate_logic_rejects_invalid_sequences() -> None:
    core = FormulaEngineCore()
    res = core.validate_logic("1 + *** 2")
    assert res["is_valid"] is False
    assert "error" in res


def test_validate_logic_accepts_basic_formula() -> None:
    core = FormulaEngineCore()
    res = core.validate_logic("{a}+{b}*2")
    assert res["is_valid"] is True
    assert res["error"] is None
