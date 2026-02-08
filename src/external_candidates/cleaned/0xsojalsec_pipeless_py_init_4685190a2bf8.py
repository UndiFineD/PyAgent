# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\yolo.py\init_4685190a2bf8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\yolo\init.py

from ultralytics import YOLO


def init():
    return {"model": YOLO("yolov8n.pt")}
