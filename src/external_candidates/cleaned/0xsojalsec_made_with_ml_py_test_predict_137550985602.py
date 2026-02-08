# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_made_with_ml.py\tests.py\code.py\test_predict_137550985602.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Made-With-ML\tests\code\test_predict.py

from madewithml import predict


def test_decode():

    decoded = predict.decode(indices=[0, 1, 1], index_to_class={0: "x", 1: "y"})

    assert decoded == ["x", "y", "y"]


def test_format_prob():

    d = predict.format_prob(prob=[0.1, 0.9], index_to_class={0: "x", 1: "y"})

    assert d == {"x": 0.1, "y": 0.9}
