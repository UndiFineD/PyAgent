# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\utils\submission.py
import os

from ovo import NextflowScheduler, schedulers

test_scheduler_key = os.getenv("OVO_TEST_SCHEDULER")
if not test_scheduler_key:
    options = [f"OVO_TEST_SCHEDULER={k}" for k in schedulers.keys()]
    raise ValueError(f"Run tests with one of: {' '.join(options)}")

if test_scheduler_key not in schedulers:
    raise ValueError(
        f"Expected OVO_TEST_SCHEDULER to be one of {list(schedulers.keys())}, but got '{test_scheduler_key}'"
    )

test_scheduler: NextflowScheduler = schedulers[test_scheduler_key]
