# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\onnx_candy.py\pre_process_21385dddec0e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\onnx-candy\pre-process.py

import cv2

import numpy as np


def hook(frame_data, _):
    frame = frame_data["original"]

    ih, iw = (224, 224)

    h, w, _ = frame.shape

    scale = min(iw / w, ih / h)

    nw, nh = int(scale * w), int(scale * h)

    image_resized = cv2.resize(frame, (nw, nh))

    image_padded = np.full(shape=[ih, iw, 3], fill_value=128.0)

    dw, dh = (iw - nw) // 2, (ih - nh) // 2

    image_padded[dh : nh + dh, dw : nw + dw, :] = image_resized

    image_padded = image_padded / 255.0

    image_padded = image_padded.astype(np.float32)

    image_padded = np.transpose(image_padded, axes=(2, 0, 1))  # Convert to c,h,w

    frame_data["inference_input"] = image_padded
