# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\cats.py\init_1895c3ba445d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\cats\init.py

import cv2


def init():
    return {"model": cv2.CascadeClassifier("/home/path/pipeless/examples/cats/cats.xml")}
