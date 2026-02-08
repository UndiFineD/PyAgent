# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\mediapipe\run_mp.py
import os

import cv2
import mediapipe as mp
import numpy as np
from draw_util_refine import FaceMeshVisualizer
from mp_utils_refine import LMKExtractor
from pose_util import (
    euler_and_translation_to_matrix,
    matrix_to_euler_and_translation,
    project_points,
    project_points_with_trans,
    smooth_pose_seq,
)
from tqdm import trange

mp_face_mesh = mp.solutions.face_mesh


def extract_and_draw_lmks(input_file, output_file):
    ref_lmk_extractor = LMKExtractor()
    lmk_extractor = LMKExtractor()
    vis = FaceMeshVisualizer()

    cap = cv2.VideoCapture(input_file)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (3 * width, height))
    write_ref_img = False

    RE = [
        384,
        385,
        386,
        387,
        388,
        390,
        263,
        362,
        398,
        466,
        373,
        374,
        249,
        380,
        381,
        382,
    ]
    LE = [160, 33, 161, 163, 133, 7, 173, 144, 145, 246, 153, 154, 155, 157, 158, 159]

    for i in trange(200):
        ret, frame = cap.read()

        if not ret:
            break

        ref_result = ref_lmk_extractor(cv2.imread("big_face.png"))
        tgt_result = lmk_extractor(frame)

        init_tran_vec = ref_result["trans_mat"][:3, 3]

        if tgt_result is not None:
            lmks = tgt_result["lmks"].astype(np.float32)
            lmks3d = tgt_result["lmks3d"].astype(np.float32)

            LE_kps = lmks[LE]
            RE_kps = lmks[RE]

            iris_left = lmks[468]
            iris_right = lmks[473]

            IRIS_L_x = (iris_left[0] - LE_kps[:, 0].min()) / (LE_kps[:, 0].max() - LE_kps[:, 0].min())
            IRIS_L_y = (iris_left[1] - LE_kps[:, 1].min()) / (LE_kps[:, 1].max() - LE_kps[:, 1].min())
            IRIS_R_x = (iris_right[0] - RE_kps[:, 0].min()) / (RE_kps[:, 0].max() - RE_kps[:, 0].min())
            IRIS_R_y = (iris_right[1] - RE_kps[:, 1].min()) / (RE_kps[:, 1].max() - RE_kps[:, 1].min())

            euler_angles, translation_vector = matrix_to_euler_and_translation(tgt_result["trans_mat"])
            pose = np.concatenate((euler_angles, translation_vector), 0)

            lmks3d = np.array([lmks3d])
            pose = np.array([pose])

            pose[:, 3:6] = init_tran_vec
            new_pose = euler_and_translation_to_matrix(pose[0][:3], pose[0][3:6])
            # lmks_trans = project_points(lmks3d, ref_result['trans_mat'], new_pose, [frame.shape[0],frame.shape[1]])
            lmks_trans = project_points_with_trans(lmks3d, new_pose, [frame.shape[0], frame.shape[1]])

            IRIS_L_tran_x = lmks_trans[0][LE][:, 0].min() + IRIS_L_x * (
                lmks_trans[0][LE][:, 0].max() - lmks_trans[0][LE][:, 0].min()
            )
            IRIS_L_tran_y = lmks_trans[0][LE][:, 1].min() + IRIS_L_y * (
                lmks_trans[0][LE][:, 1].max() - lmks_trans[0][LE][:, 1].min()
            )
            IRIS_R_tran_x = lmks_trans[0][RE][:, 0].min() + IRIS_R_x * (
                lmks_trans[0][RE][:, 0].max() - lmks_trans[0][RE][:, 0].min()
            )
            IRIS_R_tran_y = lmks_trans[0][RE][:, 1].min() + IRIS_R_y * (
                lmks_trans[0][RE][:, 1].max() - lmks_trans[0][RE][:, 1].min()
            )
            L_IRIS = [IRIS_L_tran_x, IRIS_L_tran_y]
            R_IRIS = [IRIS_R_tran_x, IRIS_R_tran_y]

            lmk_img = vis.draw_landmarks(
                (frame.shape[1], frame.shape[0]),
                lmks,
                L_E=lmks[468],
                R_E=lmks[473],
                normed=True,
            )
            tra_lmk_img = vis.draw_landmarks(
                (frame.shape[1], frame.shape[0]),
                lmks_trans[0],
                L_E=L_IRIS,
                R_E=R_IRIS,
                normed=True,
            )
            ref_lmk_img = vis.draw_landmarks(
                (frame.shape[1], frame.shape[0]),
                ref_result["lmks"],
                L_E=ref_result["lmks"][468],
                R_E=ref_result["lmks"][473],
                normed=True,
            )

            debug_img = np.concatenate((ref_lmk_img, lmk_img, tra_lmk_img), 1)
            out.write(debug_img)
            cv2.imwrite("debug/debug_%05d.jpg" % i, debug_img)
        else:
            print("multiple faces in the frame")
    out.release()


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    input_file = "gaze.mp4"
    lmk_video_path = "./pose.mp4"

    # crop video
    # crop_video(input_file, output_file)

    # extract and draw lmks
    extract_and_draw_lmks(input_file, lmk_video_path)
