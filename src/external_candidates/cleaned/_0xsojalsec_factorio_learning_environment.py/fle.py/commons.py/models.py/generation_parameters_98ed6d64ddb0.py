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
