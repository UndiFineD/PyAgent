# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\mediapipe\draw_mp.py
import os
import pdb

import cv2
import mediapipe as mp
import numpy as np
import torch
from tqdm import trange
from utils.draw_util_refine import FaceMeshVisualizer
from utils.mp_utils_refine import LMKExtractor
from utils.pose_util import (
    euler_and_translation_to_matrix,
    invert_projection,
    matrix_to_euler_and_translation,
    project_points,
    project_points_with_trans,
    smooth_pose_seq,
)

mp_face_mesh = mp.solutions.face_mesh
import copy


def get_semantic_indices():
    mp_connections = mp.solutions.face_mesh_connections

    semantic_connections = {
        "Contours": mp_connections.FACEMESH_CONTOURS,
        "FaceOval": mp_connections.FACEMESH_FACE_OVAL,
        "LeftIris": mp_connections.FACEMESH_LEFT_IRIS,
        "LeftEye": mp_connections.FACEMESH_LEFT_EYE,
        "LeftEyebrow": mp_connections.FACEMESH_LEFT_EYEBROW,
        "RightIris": mp_connections.FACEMESH_RIGHT_IRIS,
        "RightEye": mp_connections.FACEMESH_RIGHT_EYE,
        "RightEyebrow": mp_connections.FACEMESH_RIGHT_EYEBROW,
        "Lips": mp_connections.FACEMESH_LIPS,
        "Tesselation": mp_connections.FACEMESH_TESSELATION,
    }

    def get_compact_idx(connections):
        ret = []
        for conn in connections:
            ret.append(conn[0])
            ret.append(conn[1])

        return sorted(tuple(set(ret)))

    semantic_indexes = {k: get_compact_idx(v) for k, v in semantic_connections.items()}

    return semantic_indexes


def move_kp_to_center(kps):
    center_kps = kps - kps.mean(0) + [0.5, 0.5, 0.5]
    scale = center_kps.max(0) - center_kps.min(0)
    y_div_x = scale[1] / scale[0]
    z_div_x = scale[2] / scale[0]
    new_x_min = 0.1
    new_x_max = 0.9
    y_len = (new_x_max - new_x_min) * y_div_x
    z_len = (new_x_max - new_x_min) * z_div_x
    new_y_min = 0.5 - y_len / 2
    new_y_max = 0.5 + y_len / 2
    new_z_min = 0.5 - z_len / 2
    new_z_max = 0.5 + z_len / 2
    kps_max = np.array([new_x_max, new_y_max, new_z_max])
    kps_min = np.array([new_x_min, new_y_min, new_z_min])
    # 归一化处理到[0, 1]之间
    min_vals = np.min(center_kps, axis=0)
    max_vals = np.max(center_kps, axis=0)
    normalized_points = (center_kps - min_vals) / (max_vals - min_vals)

    # 线性变换到kps_min和kps_max之间
    scaled_points = normalized_points * (kps_max - kps_min) + kps_min
    return scaled_points


def extract_and_draw_lmks(input_file, output_file):
    ref_lmk_extractor = LMKExtractor()
    vis = FaceMeshVisualizer()

    # cap = cv2.VideoCapture(input_file)
    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter(output_file, fourcc, fps, (3*width, height))
    write_ref_img = False
    indices = get_semantic_indices()
    LE = indices["LeftEye"]
    RE = indices["RightEye"]
    RightIris = indices["RightIris"]
    LeftIris = indices["LeftIris"]

    frame = cv2.imread("/home/fhong/vfhq_dataset/images/003759/0100.png")
    ref_result = ref_lmk_extractor(frame)
    ref_lmk_img = vis.draw_landmarks(
        (frame.shape[1], frame.shape[0]),
        ref_result["lmks"],
        L_E=ref_result["lmks"][LeftIris].mean(0),
        R_E=ref_result["lmks"][RightIris].mean(0),
        normed=True,
    )
    cv2.imwrite("debug.jpg", ref_lmk_img)

    Lips_idx = indices["Lips"]
    lmks = np.zeros_like(ref_result["lmks"]) - 0.1
    lip_value = ref_result["lmks"][Lips_idx]
    lmks[Lips_idx] = move_kp_to_center(lip_value)
    ref_lmk_img = vis.draw_landmarks(
        (frame.shape[1], frame.shape[0]),
        lmks,
        L_E=lmks[LeftIris].mean(0),
        R_E=lmks[RightIris].mean(0),
        normed=True,
    )
    cv2.imwrite("debug2.jpg", ref_lmk_img)

    LE_idx = indices["LeftEye"]
    LeftEyebrow_idx = indices["LeftEyebrow"]
    LeftIris_idx = indices["LeftIris"]
    lmks = np.zeros_like(ref_result["lmks"]) - 0.1
    LE_value = np.concatenate(
        (
            ref_result["lmks"][LE_idx],
            ref_result["lmks"][LeftEyebrow_idx],
            ref_result["lmks"][LeftIris_idx],
        ),
        0,
    )
    value = move_kp_to_center(LE_value)
    lmks[LE_idx] = value[: len(lmks[LE_idx])]
    lmks[LeftEyebrow_idx] = value[len(lmks[LE_idx]) : len(lmks[LE_idx]) + len(lmks[LeftEyebrow_idx])]
    lmks[LeftIris_idx] = value[-len(lmks[LeftIris_idx]) :]

    ref_lmk_img = vis.draw_landmarks(
        (frame.shape[1], frame.shape[0]),
        lmks,
        L_E=lmks[LeftIris].mean(0),
        R_E=lmks[RightIris].mean(0),
        normed=True,
    )
    cv2.imwrite("debug3.jpg", ref_lmk_img)


def extract_eyes_mouth(lmk, output_file):
    ref_lmk_extractor = LMKExtractor()
    vis = FaceMeshVisualizer()
    write_ref_img = False
    indices = get_semantic_indices()
    LE = indices["LeftEye"]
    RE = indices["RightEye"]
    RightIris = indices["RightIris"]
    LeftIris = indices["LeftIris"]
    frame = cv2.imread("/sensei-fs/users/fhong/src/mambaface/norm_pose/0003.png")
    height, width = frame.shape[:2]
    ref_result = ref_lmk_extractor(frame)
    lmks3d = ref_result["lmks3d"]
    trans_mat = ref_result["trans_mat"]
    lmks = ref_result["lmks"]
    euler_angles, translation_vector = matrix_to_euler_and_translation(trans_mat)
    pose_seq = np.zeros([1, 6])
    pose_seq[0, :3] = euler_angles
    pose_seq[0, 3:6] = translation_vector
    project_lmks = project_points(lmks3d[np.newaxis], np.eye(4), pose_seq, [512, 512])
    project_lmks = project_lmks[0]
    ref_lmk_img = vis.draw_landmarks(
        (frame.shape[1], frame.shape[0]),
        ref_result["lmks"],
        L_E=ref_result["lmks"][LeftIris].mean(0),
        R_E=ref_result["lmks"][RightIris].mean(0),
        normed=True,
    )
    cv2.imwrite("debug.jpg", ref_lmk_img)
    project_lmk_img2 = vis.draw_landmarks((frame.shape[1], frame.shape[0]), project_lmks, normed=True)
    cv2.imwrite("debug2.jpg", project_lmk_img2)

    cp_lmks = copy.copy(lmks)
    project_lmks3d = invert_projection(cp_lmks[np.newaxis], np.eye(4), pose_seq, [height, width])
    project_lmks2 = project_points(project_lmks3d, np.eye(4), pose_seq, [height, width])
    project_lmks2 = project_lmks2[0]
    project_lmk_img = vis.draw_landmarks(
        (frame.shape[1], frame.shape[0]),
        project_lmks2,
        L_E=project_lmks2[LeftIris].mean(0),
        R_E=project_lmks2[RightIris].mean(0),
        normed=True,
    )
    cv2.imwrite("debug3.jpg", project_lmk_img + project_lmk_img2)


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    input_file = "gaze.mp4"
    lmk_video_path = "/mnt/localssd/vfhq/test/Clip+-cyUxFgUyrY+P0+C2+F1045-1306/video.mp4"

    # crop video
    # crop_video(input_file, output_file)

    # extract and draw lmks
    extract_eyes_mouth(input_file, lmk_video_path)
