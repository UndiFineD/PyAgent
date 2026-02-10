
import pytest
import asyncio
from src.logic.agents.interpreter.safe_executor import SafeLocalInterpreter
from src.logic.agents.security.recon.domain_generator import DomainGenerator, MockLLM

@pytest.mark.asyncio
async def test_safe_executor():
    interpreter = SafeLocalInterpreter()
    # Test valid math
    res = await interpreter.execute("x = 5 + 5; x")
    assert res.result == 10
    assert res.success is True

    # Test forbidden builtin (should fail or result in name error depending on implementation)
    res = await interpreter.execute("import os; os.system('echo dangerous')")
    # If os is blocked, this imports nothing or fails
    # Our impl blocks import unless in allowed list. 'os' is NOT in allowed list.
    assert "module 'os' is not defined" in res.stderr or res.result is None

@pytest.mark.asyncio
async def test_domain_generator():
    mock = MockLLM()
    gen = DomainGenerator(mock)
    res = await gen.generate_permutations("test.com", 1)
    assert "example-test.com" in res.generated_domains
    assert res.seed_domain == "test.com"
