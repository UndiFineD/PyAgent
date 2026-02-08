# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_llms_from_scratch.py\setup.py\_02_installing_python_libraries.py\tests_b0571ecc2dcd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LLMs-from-scratch\setup\02_installing-python-libraries\tests.py

# Copyright (c) Sebastian Raschka under Apache License 2.0 (see LICENSE.txt).

# Source for "Build a Large Language Model From Scratch"

#   - https://www.manning.com/books/build-a-large-language-model-from-scratch

# Code: https://github.com/rasbt/LLMs-from-scratch

# File for internal use (unit tests)

from python_environment_check import main


def test_main(capsys):
    main()

    captured = capsys.readouterr()

    assert "FAIL" not in captured.out
