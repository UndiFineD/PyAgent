# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\test.py\unit.py\udf.py\test_preprocessing_pyudf_manager_86ecf8eb5770.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\test\unit\udf\test_preprocessing_pyudf_manager.py

import pytest

from feathr.udf._preprocessing_pyudf_manager import _PreprocessingPyudfManager

@pytest.mark.parametrize(

    "fn_name, fn_str",

    [

        ("fn_without_type_hint", "def fn_without_type_hint(a):\n  return a + 10\n"),

        (

            "fn_with_type_hint",

            "def fn_with_type_hint(a: int) -> int:\n  return a + 10\n",

        ),

        (

            "fn_with_complex_type_hint",

            "def fn_with_complex_type_hint(a: Union[int, float]) -> Union[int, float]:\n  return a + 10\n",

        ),

    ],

)

def test__parse_function_str_for_name(fn_name, fn_str):

    assert fn_name == _PreprocessingPyudfManager._parse_function_str_for_name(fn_str)

