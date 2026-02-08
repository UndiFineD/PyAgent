# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_prettymapp.py\conftest_dbba959c2478.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-prettymapp\conftest.py

import pytest


def pytest_addoption(parser):

    parser.addoption("--runlive", action="store_true", default=False, help="run live tests")


def pytest_collection_modifyitems(config, items):

    if not config.getoption("--runlive"):
        skip_live = pytest.mark.skip(reason="need --runlive option to run")

        for item in items:
            if "live" in item.keywords:
                item.add_marker(skip_live)
