# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\cats\init.py
import cv2


def init():
    return {"model": cv2.CascadeClassifier("/home/path/pipeless/examples/cats/cats.xml")}
