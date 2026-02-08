# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\dwpose\dwpose_detector.py
import os

import numpy as np
import torch

from .wholebody import Wholebody

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def resize_image(input_image, resolution):
    H, W, C = input_image.shape
    H = float(H)
    W = float(W)
    k = float(resolution) / min(H, W)
    H *= k
    W *= k
    H = int(np.round(H / 64.0)) * 64
    W = int(np.round(W / 64.0)) * 64
    img = cv2.resize(
        input_image,
        (W, H),
        interpolation=cv2.INTER_LANCZOS4 if k > 1 else cv2.INTER_AREA,
    )
    return img


def write_skeleton_json(H, W, candidate, subset, faces=None):
    candidate = np.array(candidate)
    subset = np.array(subset)

    skeleton_dict = {}

    for i in range(18):
        for n in range(len(subset)):
            index = int(subset[n][i])
            if index == -1:
                continue
            x, y = candidate[index][0:2]
            x = x * W
            y = y * H

            if "id_{:d}".format(n) in skeleton_dict.keys():
                skeleton_dict["id_{:d}".format(n)]["skeleton_{:d}".format(i)] = [x, y]
            else:
                skeleton_dict["id_{:d}".format(n)] = {"skeleton_{:d}".format(i): [x, y]}

    # landmark_dict = {}
    if faces is not None:
        # write face ldmks
        for fid, lmks in enumerate(faces):
            lmks = np.array(lmks)
            for lid, lmk in enumerate(lmks):
                x, y = lmk
                x = int(x * W)
                y = int(y * H)

                if "id_{:d}".format(fid) in skeleton_dict.keys():
                    skeleton_dict["id_{:d}".format(fid)]["ldmk_{:d}".format(lid)] = [
                        x,
                        y,
                    ]
                else:
                    skeleton_dict["id_{:d}".format(fid)] = {"ldmk_{:d}".format(lid): [x, y]}

        # skeleton_dict.update(landmark_dict)

    return skeleton_dict


class DWposeDetector:
    """
    A pose detect method for image-like data.

    Parameters:
        model_det: (str) serialized ONNX format model path,
                    such as https://huggingface.co/yzd-v/DWPose/blob/main/yolox_l.onnx
        model_pose: (str) serialized ONNX format model path,
                    such as https://huggingface.co/yzd-v/DWPose/blob/main/dw-ll_ucoco_384.onnx
        device: (str) 'cpu' or 'cuda:{device_id}'
    """

    def __init__(self, model_det, model_pose, device="cpu"):
        self.args = model_det, model_pose, device

    def release_memory(self):
        if hasattr(self, "pose_estimation"):
            del self.pose_estimation
            import gc

            gc.collect()

    def __call__(self, oriImg, write_json=False, detect_resolution=None):
        if not hasattr(self, "pose_estimation"):
            self.pose_estimation = Wholebody(*self.args)

        oriImg = oriImg.copy()
        # if detect_resolution is not None:
        #     oriImg = resize_image(oriImg, detect_resolution)
        H, W, C = oriImg.shape
        with torch.no_grad():
            candidate, score = self.pose_estimation(oriImg)
            nums, _, locs = candidate.shape
            candidate[..., 0] /= float(W)
            candidate[..., 1] /= float(H)
            body = candidate[:, :18].copy()
            body = body.reshape(nums * 18, locs)
            subset = score[:, :18].copy()
            for i in range(len(subset)):
                for j in range(len(subset[i])):
                    if subset[i][j] > 0.3:
                        subset[i][j] = int(18 * i + j)
                    else:
                        subset[i][j] = -1

            # un_visible = subset < 0.3
            # candidate[un_visible] = -1

            # foot = candidate[:, 18:24]

            faces = candidate[:, 24:92]

            hands = candidate[:, 92:113]
            hands = np.vstack([hands, candidate[:, 113:]])

            faces_score = score[:, 24:92]
            hands_score = np.vstack([score[:, 92:113], score[:, 113:]])

            bodies = dict(candidate=body, subset=subset, score=score[:, :18])
            pose = dict(
                bodies=bodies,
                hands=hands,
                hands_score=hands_score,
                faces=faces,
                faces_score=faces_score,
            )
            # import pdb; pdb.set_trace()

            if not write_json:
                return pose
            else:
                return pose, write_skeleton_json(
                    H,
                    W,
                    pose["bodies"]["candidate"],
                    pose["bodies"]["subset"],
                    faces=pose["faces"],
                )


# dwpose_detector = DWposeDetector(
#     model_det="models/DWPose/yolox_l.onnx",
#     model_pose="models/DWPose/dw-ll_ucoco_384.onnx",
#     device=device)
