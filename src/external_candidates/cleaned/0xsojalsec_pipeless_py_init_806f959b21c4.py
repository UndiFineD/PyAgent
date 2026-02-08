# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\gaze_piano.py\init_806f959b21c4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\gaze-piano\init.py

import mediapipe as mp


def init():
    # Store the face_mesh on the context to avoid starting it on every frame

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,  # number of faces to track in each frame
        refine_landmarks=True,  # includes iris landmarks in the face mesh model
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    return {
        "face_mesh": face_mesh,
    }
