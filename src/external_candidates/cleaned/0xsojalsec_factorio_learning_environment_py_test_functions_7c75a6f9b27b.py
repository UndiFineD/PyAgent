# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\test_functions_7c75a6f9b27b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\test_functions.py

import pytest


@pytest.fixture()
def game(instance):
    instance.reset()

    yield instance.namespace


def test_syntax_error(game):
    code = """

def func_1(arg):

    print("a")

    assert 1 = 2

func_1(6)

"""

    _, _, result = game.instance.eval(code)

    assert "invalid syntax" in result


def test_assertion_exception(game):
    code = """

print('a')

assert 1 == 2

"""

    _, _, result = game.instance.eval(code)

    assert "('a',)" in result

    assert "AssertionError" in result


def test_function_with_entity_annotation(game):
    code = """

def func_1(arg1: Entity) -> str:

    \"\"\"this is a func\"\"\"

    print("a")

    assert 1 == 2

def func_2():

    func_1({})

func_2()

"""

    _, _, result = game.instance.eval(code)

    assert "('a',)" in result

    assert "AssertionError" in result
