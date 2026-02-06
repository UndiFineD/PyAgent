# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\utils\controller_loader\call_info.py
from dataclasses import dataclass


@dataclass
class CallInfo:
    """Contains information about a class's __call__ method."""

    input_types: str
    output_type: str
    docstring: str
    signature: str
