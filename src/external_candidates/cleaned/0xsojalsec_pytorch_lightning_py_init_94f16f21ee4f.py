# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pytorch_lightning.py\tests.py\parity_pytorch.py\init_94f16f21ee4f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\parity_pytorch\__init__.py

import pytest

from lightning.pytorch.utilities.testing import _runif_reasons


def RunIf(**kwargs):
    reasons, marker_kwargs = _runif_reasons(**kwargs)

    return pytest.mark.skipif(
        condition=len(reasons) > 0,
        reason=f"Requires: [{' + '.join(reasons)}]",
        **marker_kwargs,
    )
