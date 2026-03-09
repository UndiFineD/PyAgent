def test_simple_benchmark():
    from benchmarks import simple

    result = simple.run()
    assert isinstance(result, dict)
    assert result.get("latency") == 0
