# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\cats.py\process_a8e8e66e62ba.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\cats\process.py

import numpy as np


def hook(frame_data, context):
    model = context["model"]

    reduced_frame = frame_data["modified"]

    bounding_boxes = model.detectMultiScale(reduced_frame, minSize=(30, 30))

    frame_data["inference_output"] = np.array(bounding_boxes).astype("float32")
