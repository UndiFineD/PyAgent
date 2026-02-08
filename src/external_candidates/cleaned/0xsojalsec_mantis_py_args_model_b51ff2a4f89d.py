# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_mantis.py\mantis.py\models.py\args_model_b51ff2a4f89d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\models\args_model.py

from typing import Literal

from pydantic import BaseModel, Field


class ArgsModel(BaseModel):
    input_type: Literal["host", "file"] = Field(None)

    input: str = Field(None)

    workflow: str = "default"

    org: str = Field(None)

    output: str = Field(None)

    app: str = Field(None)

    passive: bool = False

    stale: bool = False

    aws_profiles: list = Field(None)

    ignore_stale: bool = False

    use_ray: bool = False

    num_actors: int = 3

    delete_logs: bool = False

    verbose: bool = False

    thread_count: int = 3
