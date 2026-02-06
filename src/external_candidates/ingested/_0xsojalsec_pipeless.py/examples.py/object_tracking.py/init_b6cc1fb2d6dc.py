# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\object-tracking\init.py
from norfair import Tracker


def init():
    return {"tracker": Tracker(distance_function="euclidean", distance_threshold=50)}
