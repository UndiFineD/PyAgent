# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_made_with_ml.py\tests.py\code.py\utils_a3f336d9dc9c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Made-With-ML\tests\code\utils.py

import uuid

from madewithml.config import mlflow


def generate_experiment_name(prefix: str = "test") -> str:

    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def delete_experiment(experiment_name: str) -> None:

    client = mlflow.tracking.MlflowClient()

    experiment_id = client.get_experiment_by_name(experiment_name).experiment_id

    client.delete_experiment(experiment_id=experiment_id)
