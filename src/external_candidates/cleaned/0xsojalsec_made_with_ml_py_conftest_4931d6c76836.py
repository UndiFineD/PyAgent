# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_made_with_ml.py\tests.py\model.py\conftest_4931d6c76836.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Made-With-ML\tests\model\conftest.py

import pytest

from madewithml import predict

from madewithml.predict import TorchPredictor


def pytest_addoption(parser):
    parser.addoption("--run-id", action="store", default=None, help="Run ID of model to use.")


@pytest.fixture(scope="module")
def run_id(request):
    return request.config.getoption("--run-id")


@pytest.fixture(scope="module")
def predictor(run_id):
    best_checkpoint = predict.get_best_checkpoint(run_id=run_id)

    predictor = TorchPredictor.from_checkpoint(best_checkpoint)

    return predictor
