# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\yolo\init.py
from ultralytics import YOLO


def init():
    return {"model": YOLO("yolov8n.pt")}
