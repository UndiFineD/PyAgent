# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pipeless.py\examples.py\tf_pose.py\init_98e159b66b3d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pipeless\examples\tf-pose\init.py

from pipeless_ai_tf_models.multi_pose_estimation.lightning import (
    MultiPoseEstimationLightning,
)


def init():
    return {"model": MultiPoseEstimationLightning()}
