# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\object_tracking.py\init_b6cc1fb2d6dc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\object-tracking\init.py

from norfair import Tracker


def init():

    return {"tracker": Tracker(distance_function="euclidean", distance_threshold=50)}
