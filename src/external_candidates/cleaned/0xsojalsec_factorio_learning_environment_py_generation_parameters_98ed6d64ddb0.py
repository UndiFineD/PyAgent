# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\commons.py\models.py\generation_parameters_98ed6d64ddb0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\commons\models\generation_parameters.py

from typing import Dict, List, Optional

from pydantic import BaseModel


class GenerationParameters(BaseModel):
    model: str

    n: int = 1

    temperature: float = 0.5

    max_tokens: int = 2048

    logit_bias: Optional[Dict[str, float]] = None

    stop_sequences: Optional[List] = None

    presence_penalty: Optional[float] = 0

    frequency_penalty: Optional[float] = 0
