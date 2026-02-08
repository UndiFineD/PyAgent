# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_prettymapp.py\prettymapp.py\tests.py\test_plotting_482dd9aa3358.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-prettymapp\prettymapp\tests\test_plotting.py

from prettymapp.plotting import adjust_lightness


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")

    assert isinstance(color, tuple)

    assert len(color) == 3

    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)
