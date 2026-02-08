# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\object_tracking.py\process_25632b13799b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\object-tracking\process.py

# make stateful

import numpy as np

from norfair import Detection, draw_points


def hook(frame_data, context):
    tracker = context["tracker"]

    frame = frame_data["modified"]

    bboxes, scores, labels = frame_data["user_data"].values()

    norfair_detections = yolo_to_norfair(bboxes, scores)

    tracked_objects = tracker.update(detections=norfair_detections)

    draw_points(frame, drawables=tracked_objects)

    frame_data["modified"] = frame


def yolo_to_norfair(bboxes, scores):
    norfair_detections = []

    for i, bbox in enumerate(bboxes):
        box_corners = [[bbox[0], bbox[1]], [bbox[2], bbox[3]]]

        box_corners = np.array(box_corners)

        corners_scores = np.array([scores[i], scores[i]])

        norfair_detections.append(Detection(points=box_corners, scores=corners_scores))

    return norfair_detections
