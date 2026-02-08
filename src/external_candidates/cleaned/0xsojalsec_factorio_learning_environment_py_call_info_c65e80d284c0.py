# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\utils.py\controller_loader.py\call_info_c65e80d284c0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\utils\controller_loader\call_info.py

from dataclasses import dataclass


@dataclass
class CallInfo:
    """Contains information about a class's __call__ method."""

    input_types: str

    output_type: str

    docstring: str

    signature: str
