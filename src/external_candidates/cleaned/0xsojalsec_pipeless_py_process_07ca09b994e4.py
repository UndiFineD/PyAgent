# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\yolo.py\process_07ca09b994e4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\yolo\process.py

import numpy as np


def hook(frame, context):

    rgb_frame = frame["original"]

    model = context["model"]

    prediction = next(model(rgb_frame, stream=True))

    bboxes = prediction.boxes.data.tolist() if prediction.boxes else []

    frame["inference_output"] = np.array(bboxes, dtype="float32")
