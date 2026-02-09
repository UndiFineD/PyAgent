# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\face_align\scrfd.py
import os

import cv2
import numpy as np
import onnxruntime
import torch

# onnxruntime-gpu  1.7:cuda11.0  1.5-1.6:cuda10.2   1.2-1.4:cuda10.1
# ['weights/scrfd_500m_kps.onnx', 'weights/scrfd_2.5g_kps.onnx', 'weights/scrfd_10g_kps.onnx']
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ONNX_PATH = os.path.join(BASE_DIR, 'weights/scrfd_10g_bnkps_shape512x512.onnx')


class SCRFDONNX:
    def __init__(
        self,
        onnxmodel="checkpoints/scrfd_10g_bnkps_shape640x640.onnx",
        confThreshold=0.5,
        nmsThreshold=0.45,
        device="cuda",
    ):
        self.inpWidth = 640
        self.inpHeight = 640
        self.inpSize = 360
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.session = onnxruntime.InferenceSession(onnxmodel, None)
        if device.find("cuda") > -1:
            self.session.set_providers(["CUDAExecutionProvider"])
        elif device.find("cpu") > -1:
            self.session.set_providers(["CPUExecutionProvider"])
        input_cfg = self.session.get_inputs()[0]
        self.input_name = input_cfg.name
        outputs = self.session.get_outputs()
        self.output_names = []
        for o in [0, 3, 6, 1, 4, 7, 2, 5, 8]:
            self.output_names.append(outputs[o].name)
        # print(self.output_names)

        self.keep_ratio = True
        self.fmc = 3
        self._feat_stride_fpn = [8, 16, 32]
        self._num_anchors = 2

    def resize_image(self, srcimg):
        hw_scale = srcimg.shape[0] / srcimg.shape[1]
        if hw_scale > 1:
            newh, neww = self.inpHeight, int(self.inpWidth / hw_scale)
            if neww > self.inpSize:
                newh = int(newh * self.inpSize / neww)
                neww = self.inpSize
            padw = int((self.inpWidth - neww) * 0.5)
            padh = int((self.inpHeight - newh) * 0.5)
            img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
            img[padh : padh + newh, padw : padw + neww, :] = cv2.resize(
                srcimg,
                (neww, newh),
                dst=img[padh : padh + newh, padw : padw + neww, :],
                interpolation=cv2.INTER_CUBIC,
            )

        else:
            newh, neww = int(self.inpHeight * hw_scale) + 1, self.inpWidth
            if newh > self.inpSize:
                neww = int(neww * self.inpSize / newh)
                newh = self.inpSize
            padw = int((self.inpWidth - neww) * 0.5)
            padh = int((self.inpHeight - newh) * 0.5)
            img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
            img[padh : padh + newh, padw : padw + neww, :] = cv2.resize(
                srcimg,
                (neww, newh),
                dst=img[padh : padh + newh, padw : padw + neww, :],
                interpolation=cv2.INTER_CUBIC,
            )

        return img, newh, neww, padh, padw

    def distance2bbox(self, points, distance, max_shape=None):
        x1 = points[:, 0] - distance[:, 0]
        y1 = points[:, 1] - distance[:, 1]
        x2 = points[:, 0] + distance[:, 2]
        y2 = points[:, 1] + distance[:, 3]
        if max_shape is not None:
            x1 = x1.clamp(min=0, max=max_shape[1])
            y1 = y1.clamp(min=0, max=max_shape[0])
            x2 = x2.clamp(min=0, max=max_shape[1])
            y2 = y2.clamp(min=0, max=max_shape[0])
        return np.stack([x1, y1, x2, y2], axis=-1)

    def distance2kps(self, points, distance, max_shape=None):
        preds = []
        for i in range(0, distance.shape[1], 2):
            px = points[:, i % 2] + distance[:, i]
            py = points[:, i % 2 + 1] + distance[:, i + 1]
            if max_shape is not None:
                px = px.clamp(min=0, max=max_shape[1])
                py = py.clamp(min=0, max=max_shape[0])
            preds.append(px)
            preds.append(py)
        return np.stack(preds, axis=-1)

    def detect(self, srcimg):
        img, newh, neww, padh, padw = self.resize_image(srcimg)
        blob = cv2.dnn.blobFromImage(
            img,
            1.0 / 128,
            (self.inpWidth, self.inpHeight),
            (127.5, 127.5, 127.5),
            swapRB=True,
        )
        # Runs the forward pass to get output of the output layers
        outs = self.session.run(self.output_names, {self.input_name: blob})
        # for out in outs:
        #     print(out.shape)
        # inference output
        scores_list, bboxes_list, kpss_list = [], [], []
        for idx, stride in enumerate(self._feat_stride_fpn):
            scores = outs[idx * self.fmc][0]
            bbox_preds = outs[idx * self.fmc + 1][0] * stride
            kps_preds = outs[idx * self.fmc + 2][0] * stride
            height = blob.shape[2] // stride
            width = blob.shape[3] // stride
            anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(
                np.float32
            )
            anchor_centers = (anchor_centers * stride).reshape((-1, 2))
            if self._num_anchors > 1:
                anchor_centers = np.stack(
                    [anchor_centers] * self._num_anchors, axis=1
                ).reshape((-1, 2))

            pos_inds = np.where(scores >= self.confThreshold)[0]
            bboxes = self.distance2bbox(anchor_centers, bbox_preds)
            pos_scores = scores[pos_inds]
            pos_bboxes = bboxes[pos_inds]
            scores_list.append(pos_scores)
            bboxes_list.append(pos_bboxes)

            kpss = self.distance2kps(anchor_centers, kps_preds)
            # kpss = kps_preds
            kpss = kpss.reshape((kpss.shape[0], -1, 2))
            pos_kpss = kpss[pos_inds]
            kpss_list.append(pos_kpss)

        scores = np.vstack(scores_list).ravel()
        # bboxes = np.vstack(bboxes_list) / det_scale
        # kpss = np.vstack(kpss_list) / det_scale
        bboxes = np.vstack(bboxes_list)
        kpss = np.vstack(kpss_list)
        bboxes[:, 2:4] = bboxes[:, 2:4] - bboxes[:, 0:2]
        ratioh, ratiow = srcimg.shape[0] / newh, srcimg.shape[1] / neww
        bboxes[:, 0] = (bboxes[:, 0] - padw) * ratiow
        bboxes[:, 1] = (bboxes[:, 1] - padh) * ratioh
        bboxes[:, 2] = bboxes[:, 2] * ratiow
        bboxes[:, 3] = bboxes[:, 3] * ratioh
        kpss[:, :, 0] = (kpss[:, :, 0] - padw) * ratiow
        kpss[:, :, 1] = (kpss[:, :, 1] - padh) * ratioh
        indices = cv2.dnn.NMSBoxes(
            bboxes.tolist(), scores.tolist(), self.confThreshold, self.nmsThreshold
        )
        return (
            bboxes[indices, :].reshape(-1, 4),
            kpss[indices, :, :].reshape(-1, 5, 2),
            scores[indices].reshape(-1),
        )


class SCRFD:
    def __init__(
        self,
        pt_path="checkpoints/scrfd_10g_bnkps.pt",
        confThreshold=0.5,
        nmsThreshold=0.45,
        device="cuda",
    ):
        self.inpWidth = 640
        self.inpHeight = 640
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        torch.set_grad_enabled(False)
        self.test_device = torch.device(device if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available() and "cuda" in device:
            torch.backends.cudnn.benchmark = True

        self.model = torch.jit.load(pt_path)
        self.model.eval()
        self.model.to(self.test_device)

        self.keep_ratio = True
        self.fmc = 3
        self._feat_stride_fpn = [8, 16, 32]
        self._num_anchors = 2

    def resize_image(self, srcimg):
        padh, padw, newh, neww = 0, 0, self.inpHeight, self.inpWidth
        if self.keep_ratio and srcimg.shape[0] != srcimg.shape[1]:
            hw_scale = srcimg.shape[0] / srcimg.shape[1]
            if hw_scale > 1:
                newh, neww = self.inpHeight, int(self.inpWidth / hw_scale)
                padw = int((self.inpWidth - neww) * 0.5)
                img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
                img[:, padw : padw + neww, :] = cv2.resize(
                    srcimg, (neww, newh), dst=img[:, padw : padw + neww, :]
                )  # , interpolation=cv2.INTER_AREA)

            else:
                newh, neww = int(self.inpHeight * hw_scale) + 1, self.inpWidth
                padh = int((self.inpHeight - newh) * 0.5)
                img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
                img[padh : padh + newh, :, :] = cv2.resize(
                    srcimg, (neww, newh), dst=img[padh : padh + newh, :, :]
                )  # , interpolation=cv2.INTER_AREA)

        else:
            img = cv2.resize(
                srcimg, (self.inpWidth, self.inpHeight)
            )  # , interpolation=cv2.INTER_AREA)
        return img, newh, neww, padh, padw

    # def resize_image(self, srcimg):
    #     h,w, c = srcimg.shape
    #     hw_scale = h / w
    #     if hw_scale > 1:
    #         newh, neww = int(h*self.inpSize/w), self.inpSize
    #         self.inpWidth=neww
    #         self.inpHeight=(newh+31)//32*32
    #         padh = int((self.inpHeight - newh) * 0.5)
    #         padw = 0
    #         img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
    #         img[padh:padh+newh, :, :] = cv2.resize(srcimg, (neww, newh), dst=img[padh:padh+newh, :, :])#, interpolation=cv2.INTER_AREA)
    #
    #     else:
    #         newh, neww = self.inpSize, int(w*self.inpSize/h)
    #         self.inpWidth=(neww+31)//32*32
    #         self.inpHeight=newh
    #         padw = int((self.inpWidth - neww) * 0.5)
    #         padh = 0
    #         img = np.zeros((self.inpHeight, self.inpWidth, 3), dtype=np.uint8)
    #         img[:, padw:padw+neww,:] = cv2.resize(srcimg, (neww, newh), dst=img[:, padw:padw+neww,:])#, interpolation=cv2.INTER_AREA)
    #     return img, newh, neww, padh, padw

    def distance2bbox(self, points, distance, max_shape=None):
        x1 = points[:, 0] - distance[:, 0]
        y1 = points[:, 1] - distance[:, 1]
        x2 = points[:, 0] + distance[:, 2]
        y2 = points[:, 1] + distance[:, 3]
        if max_shape is not None:
            x1 = x1.clamp(min=0, max=max_shape[1])
            y1 = y1.clamp(min=0, max=max_shape[0])
            x2 = x2.clamp(min=0, max=max_shape[1])
            y2 = y2.clamp(min=0, max=max_shape[0])
        return np.stack([x1, y1, x2, y2], axis=-1)

    def distance2kps(self, points, distance, max_shape=None):
        preds = []
        for i in range(0, distance.shape[1], 2):
            px = points[:, i % 2] + distance[:, i]
            py = points[:, i % 2 + 1] + distance[:, i + 1]
            if max_shape is not None:
                px = px.clamp(min=0, max=max_shape[1])
                py = py.clamp(min=0, max=max_shape[0])
            preds.append(px)
            preds.append(py)
        return np.stack(preds, axis=-1)

    def detect(self, srcimg):
        img, newh, neww, padh, padw = self.resize_image(srcimg)

        input_tensor = torch.from_numpy(
            img[:, :, [2, 1, 0]].transpose(2, 0, 1).astype(np.float32)
        ).unsqueeze(0)
        # Runs the forward pass to get output of the output layers
        results = self.model(input_tensor.to(self.test_device) / 127.5 - 1)

        outs = []
        for i in [0, 3, 6, 1, 4, 7, 2, 5, 8]:
            outs.append(results[i].cpu().numpy())
        # for out in outs:
        #     print(out.shape)
        # inference output
        scores_list, bboxes_list, kpss_list = [], [], []
        for idx, stride in enumerate(self._feat_stride_fpn):
            scores = outs[idx * self.fmc][0]
            bbox_preds = outs[idx * self.fmc + 1][0] * stride
            kps_preds = outs[idx * self.fmc + 2][0] * stride
            height = self.inpHeight // stride
            width = self.inpWidth // stride
            anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(
                np.float32
            )
            anchor_centers = (anchor_centers * stride).reshape((-1, 2))
            if self._num_anchors > 1:
                anchor_centers = np.stack(
                    [anchor_centers] * self._num_anchors, axis=1
                ).reshape((-1, 2))

            pos_inds = np.where(scores >= self.confThreshold)[0]
            bboxes = self.distance2bbox(anchor_centers, bbox_preds)
            pos_scores = scores[pos_inds]
            pos_bboxes = bboxes[pos_inds]
            scores_list.append(pos_scores)
            bboxes_list.append(pos_bboxes)

            kpss = self.distance2kps(anchor_centers, kps_preds)
            # kpss = kps_preds
            kpss = kpss.reshape((kpss.shape[0], -1, 2))
            pos_kpss = kpss[pos_inds]
            kpss_list.append(pos_kpss)

        scores = np.vstack(scores_list).ravel()
        # bboxes = np.vstack(bboxes_list) / det_scale
        # kpss = np.vstack(kpss_list) / det_scale
        bboxes = np.vstack(bboxes_list)
        kpss = np.vstack(kpss_list)
        bboxes[:, 2:4] = bboxes[:, 2:4] - bboxes[:, 0:2]
        ratioh, ratiow = srcimg.shape[0] / newh, srcimg.shape[1] / neww
        bboxes[:, 0] = (bboxes[:, 0] - padw) * ratiow
        bboxes[:, 1] = (bboxes[:, 1] - padh) * ratioh
        bboxes[:, 2] = bboxes[:, 2] * ratiow
        bboxes[:, 3] = bboxes[:, 3] * ratioh
        kpss[:, :, 0] = (kpss[:, :, 0] - padw) * ratiow
        kpss[:, :, 1] = (kpss[:, :, 1] - padh) * ratioh
        indices = cv2.dnn.NMSBoxes(
            bboxes.tolist(), scores.tolist(), self.confThreshold, self.nmsThreshold
        )
        return (
            bboxes[indices, :].reshape(-1, 4),
            kpss[indices, :, :].reshape(-1, 5, 2),
            scores[indices].reshape(-1),
        )


if __name__ == "__main__":
    import time

    imgpath = "test.png"

    # mynetpt = SCRFD(pt_path='../checkpoints/scrfd_10g_bnkps.pt', confThreshold=0.5, nmsThreshold=0.45)
    mynetonnx = SCRFDONNX(
        onnxmodel="../checkpoints/scrfd_10g_bnkps_shape640x640.onnx",
        confThreshold=0.5,
        nmsThreshold=0.45,
    )

    srcimg = cv2.imread(imgpath)

    # warm up
    bboxes, kpss, scores = mynetonnx.detect(srcimg)
    bboxes, kpss, scores = mynetonnx.detect(srcimg)
    bboxes, kpss, scores = mynetonnx.detect(srcimg)

    t1 = time.time()
    for _ in range(10):
        bboxes, kpss, scores = mynetonnx.detect(srcimg)
    t2 = time.time()
    print("total time: {} ms".format((t2 - t1) * 1000))

    # t1 = time.time()
    # for _ in range(10):
    #     bboxes, kpss, scores = mynetpt.detect(srcimg)
    # t2 = time.time()
    # print('total time: {} ms'.format((t2 - t1) * 1000))
    #
    # print(np.equal(bboxes0, bboxes))
    # print(np.equal(kpss0, kpss))
    # print(np.equal(scores0, scores))

    print(bboxes.shape)
    for i in range(bboxes.shape[0]):
        xmin, ymin, xamx, ymax = (
            int(bboxes[i, 0]),
            int(bboxes[i, 1]),
            int(bboxes[i, 0] + bboxes[i, 2]),
            int(bboxes[i, 1] + bboxes[i, 3]),
        )
        cv2.rectangle(srcimg, (xmin, ymin), (xamx, ymax), (0, 0, 255), thickness=2)
        for j in range(5):
            cv2.circle(
                srcimg,
                (int(kpss[i, j, 0]), int(kpss[i, j, 1])),
                1,
                (0, 255, 0),
                thickness=-1,
            )
        # cv2.putText(srcimg, str(round(scores[i], 3)), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
        #             thickness=1)

    # cv2.imshow('111', srcimg)
    # cv2.waitKey(0)
    cv2.imwrite("test_scrfd.jpg", srcimg)
