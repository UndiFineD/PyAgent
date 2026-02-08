# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\face_align\align.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import pdb

import numpy as np
import torch

from .align_tools import points_117_158_256

# import load_model
from .utils import (
    align_N,
    align_N_aug,
    align_N_picasso_aug3,
    cvt130PtsTo94Pts,
    cvt256PtsTo94Pts,
    inv_affine,
    landmark_warpAffine,
    read_pts,
)

# from .scrfd import SCRFDONNX
from .yoloface import YoloFace


def phase1(device, p1_path):
    align_w = 256
    align_h = 256
    net_scale = 1.1
    in_channel = 3
    meanf = os.path.join(BASE_DIR, "meanfiles/mean_pts130_scale112_full_flip_phase1.txt")
    # model_path = os.path.join(BASE_DIR, 'weights/p1.pt')
    # model_path = os.path.join(BASE_DIR, 'models/1202_dzg/p1.pkl')
    mean_ld = read_pts(meanf) * [align_h / 112.0, align_w / 112.0]
    model = torch.jit.load(p1_path)
    model.to(device)
    model.eval()
    return model, mean_ld, align_w, align_h, net_scale, in_channel


def phase2(device, p2_path):
    align_w = 256
    align_h = 256
    net_scale = 1.5
    in_channel = 9
    meanf = os.path.join(BASE_DIR, "meanfiles/mean_pts130_scale112_full_flip_phase2.txt")
    # model_path = os.path.join(BASE_DIR, 'weights/p2.pt')
    # model_path = os.path.join(BASE_DIR, 'models/1202_dzg/p2.pkl')
    mean_ld = read_pts(meanf) * [align_h / 112.0, align_w / 112.0]

    """
    img = np.zeros((256, 256, 3))
    utils.draw_pts(img, mean_ld)
    cv2.imwrite('mean.jpg', img)
    """

    model = torch.jit.load(p2_path)
    model.to(device)
    model.eval()
    return model, mean_ld, align_w, align_h, net_scale, in_channel


def cvt221PtsTo130Pts(pts221):
    pts130 = []
    j = -1
    # eyebrow
    for i in range(0, 16 * 2):
        j += 1
        if i % 2:
            continue
        pts130.append(pts221[j])
    # eye
    for i in range(0, 24 * 2):
        j += 1
        if i % 3:
            continue
        pts130.append(pts221[j])
    # nose
    for i in range(0, 22):
        j += 1
        pts130.append(pts221[j])
    # mouth
    for i in range(0, 72):
        j += 1
        if i % 3 or i == 36 or i == 54:
            continue
        pts130.append(pts221[j])
    # profile
    for i in range(0, 41):
        j += 1
        pts130.append(pts221[j])

    # forehead
    for i in range(0, 7):
        pts130.append(np.array([0, 0]))

    # pupil
    for i in range(0, 6):
        pts130.append(np.array([0, 0]))

    pts130 = np.array(pts130)
    return pts130


def cvt221PtsTo228Pts(pts221):
    pts228 = []
    j = -1
    # eye
    for i in range(0, 40 * 2):
        j += 1
        pts228.append(pts221[j])
    # nose
    for i in range(0, 22):
        j += 1
        pts228.append(pts221[j])

    # mouth
    for i in range(0, 72):
        j += 1
        pts228.append(pts221[j])

    # profile
    for i in range(0, 41):
        j += 1
        pts228.append(pts221[j])

    # forehead
    for i in range(0, 7):
        pts228.append(np.array([0, 0]))

    # pupil
    for i in range(0, 6):
        j += 1
        pts228.append(pts221[j])
    pts228 = np.array(pts228)
    return pts228


def cvt_pts(pts221):
    pred_p2_eye = pts221[0:80, :]
    pred_p1_nose = pts221[80:102, :]
    pred_p2_mouth = pts221[102:174, :]
    pred_p1_profile = pts221[174:215, :]
    pred_p2_pupil = pts221[215:221, :]

    pred_p2 = np.concatenate((pred_p2_eye, pred_p2_mouth, pred_p2_pupil))

    pts221 = np.concatenate(
        (
            pred_p2[0:16, :],
            pred_p2[43:59, :],
            pred_p2[16:40, :],
            pred_p2[59:83, :],
            pred_p1_nose,
            pred_p2[86:158, :],
            pred_p1_profile,
            pred_p2[40:41, :],
            pred_p2[83:84, :],
            pred_p2[41:43, :],
            pred_p2[84:86, :],
        ),
        axis=0,
    )

    # pts130 = cvt221PtsTo130Pts(pts221)
    # pts228 = cvt221PtsTo228Pts(pts221)
    # pts = np.concatenate((pts228, pts130))
    return pts221


class RefinePts(object):
    def __init__(self, device="cuda", p1_path="checkpoints/p1.pt", p2_path="checkpoints/p2.pt"):
        self.test_device = torch.device(device if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available() and "cuda" in device:
            torch.backends.cudnn.benchmark = True

        (
            self.model1,
            self.mean_ld1,
            self.net1_w,
            self.net1_h,
            self.net1_scale,
            self.net1_c,
        ) = phase1(self.test_device, p1_path)
        (
            self.model2,
            self.mean_ld2,
            self.net2_w,
            self.net2_h,
            self.net2_scale,
            self.net2_c,
        ) = phase2(self.test_device, p2_path)

        self.mean_ld0 = read_pts(os.path.join(BASE_DIR, "meanfiles/face_mean_5.txt")) * [
            self.net1_w / 112.0,
            self.net1_h / 112.0,
        ]

    # return 221 points
    @torch.no_grad()
    def __call__(self, im_cv2, pts_list):
        pts_res_list = []
        pts_score_list = []
        for pts in pts_list:
            pre_face = False
            pre_pts = None
            dup = 0
            pre_conf1 = 0
            pre_conf2 = 0
            while dup < 3:
                dup += 1
                cur_pts_p1 = []
                cur_vis_p1 = []
                cur_pts_p2 = []
                cur_vis_p2 = []

                img = im_cv2
                if pre_pts is None:
                    pre_pts = pts
                    face, M = align_N(
                        img,
                        pre_pts,
                        self.mean_ld0,
                        self.net1_h,
                        self.net1_w,
                        rnd_scale=self.net1_scale,
                    )
                    # cv2.imwrite('show_dir/{}_face.jpg'.format(cnt), face)
                else:
                    pre_pts = pre_pts[:117]
                    face, M = align_N_aug(
                        img,
                        pre_pts,
                        self.mean_ld1,
                        self.net1_h,
                        rnd_scale=self.net1_scale,
                    )

                # phase1
                face = np.reshape(face, (face.shape[0], face.shape[1], self.net1_c))
                face = np.float32(face)
                x = face / 128.0 - 1.0
                x = x.transpose((2, 0, 1))
                x = np.expand_dims(x, axis=0)
                x = torch.from_numpy(x)
                x = x.float().to(self.test_device)

                pts_phase1, pred_label, vis_phase1 = self.model1(x)
                label = torch.sigmoid(pred_label)
                label = label.cpu().numpy()[0][0]

                res = pts_phase1.cpu().numpy()[0]
                for i in range(len(res) // 2):
                    origin = np.float32([res[2 * i], res[2 * i + 1]])
                    cur_pts_p1.append(origin)
                cur_pts_p1 = np.asarray(cur_pts_p1)
                # cur_vis_p1 = torch.sigmoid(vis_phase1).cpu().numpy()[0]
                M_ = inv_affine(M)
                cur_pts_p1 = landmark_warpAffine(cur_pts_p1, M_)

                # phase2
                parts, M, _ = align_N_picasso_aug3(
                    img,
                    cur_pts_p1[:76],
                    self.mean_ld2,
                    self.net2_h,
                    rnd_scale=self.net2_scale,
                )
                for i in range(3):
                    parts[i] = parts[i][:, :, np.newaxis]
                face2 = np.concatenate((parts[0], parts[1], parts[2]), axis=-1)
                face2 = np.reshape(face2, (face2.shape[0], face2.shape[1], self.net2_c))
                face2 = np.float32(face2)
                x = face2 / 128.0 - 1.0
                x = x.transpose((2, 0, 1))
                x = np.expand_dims(x, axis=0)
                x = torch.from_numpy(x)
                x = x.float().to(self.test_device)
                pts_phase2, vis_phase2 = self.model2(x)
                res = pts_phase2.cpu().numpy()[0]
                for i in range(len(res) // 2):
                    origin = np.float32([res[2 * i], res[2 * i + 1]])
                    cur_pts_p2.append(origin)
                cur_pts_p2 = np.asarray(cur_pts_p2)
                # cur_vis_p2 = torch.sigmoid(vis_phase2).cpu().numpy()[0]
                M = np.array(M)
                M_ = M.copy()
                for i in range(3):
                    M_[i] = inv_affine(M[i])[:2]
                cur_pts_p2[0:43] = landmark_warpAffine(cur_pts_p2[0:43], M_[0])
                cur_pts_p2[43:86] = landmark_warpAffine(cur_pts_p2[43:86], M_[1])
                cur_pts_p2[86:158] = landmark_warpAffine(cur_pts_p2[86:158], M_[2])

                # update
                pre_pts = cur_pts_p1

                pre_face = True
                if abs(label - pre_conf1) < 0.0001 and abs(pre_conf2 - pre_conf1) < 0.0001 and label > 0.85:
                    break
                pre_conf2 = pre_conf1
                pre_conf1 = label

            if pre_face:
                pts_score_list.append(pre_conf1)
                # cur_pts = np.concatenate((cur_pts_p2[0:80, :], cur_pts_p1[32:54, :], cur_pts_p2[80:152, :], cur_pts_p1[76:117, :], cur_pts_p2[152:158, :]), axis=0)
                # #
                # # cur_vis = np.concatenate(
                # #     (cur_vis_p2[0:80], cur_vis_p1[32:54], cur_vis_p2[80:152], cur_vis_p1[76:117], cur_vis_p2[152:158]),
                # #     axis=0)
                # #
                # # cur_vis = np.array([np.array([cur_vis[i], cur_vis[i]]) for i in range(0, len(cur_vis))])
                # #
                # cur_pts = cvt_pts(cur_pts)
                # cur_vis = cvt_pts(cur_vis)
                # cur_pts = cvt_pts(cur_pts)
                #
                # cur_pts = cvt256PtsTo94Pts(cur_pts)
                # cur_pts = cvt130PtsTo94Pts(cur_pts_p1)
                # merge -> 256
                cur_pts_p2 = np.concatenate(
                    (
                        cur_pts_p2[0:16, :],
                        cur_pts_p2[43:59, :],
                        cur_pts_p2[16:40, :],
                        cur_pts_p2[59:83, :],
                        cur_pts_p2[86:158, :],
                        cur_pts_p2[40:41, :],
                        cur_pts_p2[83:84, :],
                        cur_pts_p2[41:43, :],
                        cur_pts_p2[84:86, :],
                    ),
                    axis=0,
                )
                cur_pts_p1 = np.squeeze(cur_pts_p1.reshape(117 * 2, 1))
                cur_pts_p2 = np.squeeze(cur_pts_p2.reshape(158 * 2, 1))
                face_pts = points_117_158_256(cur_pts_p2, cur_pts_p1)
                cur_pts = np.asarray(face_pts).reshape(int(len(face_pts) / 2), 2)

                pts_res_list.append(cur_pts)

        return pts_res_list, pts_score_list


class AlignImage(object):
    def __init__(
        self,
        device="cuda",
        det_path="checkpoints/yoloface_v5l.pt",
        p1_path="checkpoints/p1.pt",
        p2_path="checkpoints/p2.pt",
    ):
        # self.facedet = SCRFDONNX(onnxmodel=det_path, confThreshold=0.5, nmsThreshold=0.45, device=device)
        self.facedet = YoloFace(pt_path=det_path, confThreshold=0.5, nmsThreshold=0.45, device=device)
        self.align = RefinePts(device=device, p1_path=p1_path, p2_path=p2_path)

    @torch.no_grad()
    def __call__(self, im, maxface=False, ptstype="256"):
        # by default , face detection resize image height to 640
        # h,w,c= im.shape
        bboxes, kpss, scores = self.facedet.detect(im)
        face_num = bboxes.shape[0]
        # print('det face num : ', face_num)

        five_pts_list = []
        scores_list = []
        bboxes_list = []
        for i in range(face_num):
            five_pts_list.append(kpss[i].reshape(5, 2))
            scores_list.append(scores[i])
            bboxes_list.append(bboxes[i])

        if maxface and face_num > 1:
            max_idx = 0
            max_area = (bboxes[0, 2]) * (bboxes[0, 3])
            for i in range(1, face_num):
                area = (bboxes[i, 2]) * (bboxes[i, 3])
                if area > max_area:
                    max_idx = i
            five_pts_list = [five_pts_list[max_idx]]
            scores_list = [scores_list[max_idx]]
            bboxes_list = [bboxes_list[max_idx]]

        if ptstype == "5":
            return five_pts_list, scores_list, bboxes_list

        ytpts_list, scores_list = self.align(im, five_pts_list)

        if ptstype == "94":
            pts94_list = [cvt256PtsTo94Pts(pts) for pts in ytpts_list]
            return pts94_list, scores_list, bboxes_list

        return ytpts_list, scores_list, bboxes_list
