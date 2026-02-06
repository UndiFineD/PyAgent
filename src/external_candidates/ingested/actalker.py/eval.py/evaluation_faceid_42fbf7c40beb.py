# Extracted from: C:\DEV\PyAgent\.external\ACTalker\eval\evaluation_faceid.py
import os
import sys

sys.path.append("/apdcephfs_jn/share_302243908/ethanyichen/svd_work/SVD-Portrait")
sys.path.append(
    "/apdcephfs_cq8/share_1367250/zhentaoyu/Driving/00_VASA/01_exp/vasa09/VASA"
)
import fnmatch
import glob
import multiprocessing
import pickle
from argparse import ArgumentParser

import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import yaml
from decord import VideoReader
from deepface import DeepFace
from modules.model import senet as SENet
from PIL import Image
from scipy import linalg
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from src.utils.face_align import AlignImage

device_id = -1
device = "cuda:{}".format(device_id) if device_id > -1 else "cpu"
BASE_DIR = "/apdcephfs_jn/share_302243908/1_public_model_weights/yt_align/"
det_path = os.path.join(BASE_DIR, "yoloface_v5l.pt")
p1_path = os.path.join(BASE_DIR, "p1.pt")
p2_path = os.path.join(BASE_DIR, "p2.pt")
align_instance = AlignImage(device, det_path=det_path, p1_path=p1_path, p2_path=p2_path)


def load_state_dict(model, fname):
    """
    Set parameters converted from Caffe models authors of VGGFace2 provide.
    See https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/.

    Arguments:
        model: model
        fname: file name of parameters converted from a Caffe model, assuming the file format is Pickle.
    """
    with open(fname, "rb") as f:
        weights = pickle.load(f, encoding="latin1")

    own_state = model.state_dict()
    for name, param in weights.items():
        if name in own_state:
            try:
                own_state[name].copy_(torch.from_numpy(param))
            except Exception:
                raise RuntimeError(
                    "While copying the parameter named {}, whose dimensions in the model are {} and whose "
                    "dimensions in the checkpoint are {}.".format(
                        name, own_state[name].size(), param.size()
                    )
                )
        else:
            raise KeyError('unexpected key "{}" in state_dict'.format(name))


def process_bbox(bbox, expand_radio, height, width):
    """
    raw_vid_path:
    bbox: format: x1, y1, x2, y2
    radio: expand radio against bbox size
    height,width: source image height and width
    """

    def expand(bbox, ratio, height, width):

        bbox_h = bbox[3] - bbox[1]
        bbox_w = bbox[2] - bbox[0]

        expand_x1 = max(bbox[0] - ratio * bbox_w, 0)
        expand_y1 = max(bbox[1] - ratio * bbox_h, 0)
        expand_x2 = min(bbox[2] + ratio * bbox_w, width)
        expand_y2 = min(bbox[3] + ratio * bbox_h, height)

        return [expand_x1, expand_y1, expand_x2, expand_y2]

    def to_square(bbox_src, bbox_expend, height, width):

        h = bbox_expend[3] - bbox_expend[1]
        w = bbox_expend[2] - bbox_expend[0]
        c_h = (bbox_expend[1] + bbox_expend[3]) / 2
        c_w = (bbox_expend[0] + bbox_expend[2]) / 2

        c = min(h, w) / 2

        c_src_h = (bbox_src[1] + bbox_src[3]) / 2
        c_src_w = (bbox_src[0] + bbox_src[2]) / 2

        s_h, s_w = 0, 0
        if w < h:
            d = abs((h - w) / 2)
            s_h = min(d, abs(c_src_h - c_h))
            s_h = s_h if c_src_h > c_h else s_h * (-1)
        else:
            d = abs((h - w) / 2)
            s_w = min(d, abs(c_src_w - c_w))
            s_w = s_w if c_src_w > c_w else s_w * (-1)

        c_h = (bbox_expend[1] + bbox_expend[3]) / 2 + s_h
        c_w = (bbox_expend[0] + bbox_expend[2]) / 2 + s_w

        square_x1 = c_w - c
        square_y1 = c_h - c
        square_x2 = c_w + c
        square_y2 = c_h + c

        return [round(square_x1), round(square_y1), round(square_x2), round(square_y2)]

    bbox_expend = expand(bbox, expand_radio, height=height, width=width)
    processed_bbox = to_square(bbox, bbox_expend, height=height, width=width)

    return processed_bbox


class HumanTalkingVideoDataset(Dataset):
    def __init__(self, video_path, transform, det_head):
        super().__init__()
        self.video_path = video_path
        self.transform = transform
        self.video_reader = VideoReader(video_path)
        self.bbox_s = None
        self.det_head = det_head

    def __len__(self):
        return len(self.video_reader)

    def __getitem__(self, index):
        video_reader = VideoReader(self.video_path)
        image = video_reader[index].asnumpy()
        pil_image = Image.fromarray(image.astype(np.uint8))

        if self.bbox_s is None:
            h, w = pil_image.size
            if self.det_head:
                area = 1.2
                _, _, bboxes_list = align_instance(
                    np.array(pil_image)[:, :, [2, 1, 0]], maxface=True, ptstype="5"
                )
                try:
                    x1, y1, ww, hh = bboxes_list[0]
                    # print(self.video_path)
                except:
                    x1, y1, ww, hh = 0, 0, w, h
                x2, y2 = x1 + ww, y1 + hh
                ww, hh = (x2 - x1) * area, (y2 - y1) * area
                center = [(x2 + x1) // 2, (y2 + y1) // 2]
                x1 = max(center[0] - ww // 2, 0)
                y1 = max(center[1] - hh // 2, 0)
                x2 = min(center[0] + ww // 2, w)
                y2 = min(center[1] + hh // 2, h)
                bbox = x1, y1, x2, y2
                bbox_s = process_bbox(bbox, expand_radio=0.4, height=h, width=w)
            else:
                bbox_s = [0, 0, w, h]
            x1, y1, x2, y2 = bbox_s
            self.bbox_s = bbox_s
        else:
            x1, y1, x2, y2 = self.bbox_s

        pil_image = pil_image.crop((x1, y1, x2, y2))
        # pil_image.save('crop.png')
        tensor_image = self.transform(pil_image)
        return tensor_image


def find_data_files(directory, prefix):
    mp4_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, prefix):
            mp4_files.append(os.path.join(root, filename))
    return mp4_files


def op_eval_psnr():
    pass


def vggface2(pretrained=True):
    vggface = SENet.senet50(num_classes=8631, include_top=True)
    load_state_dict(
        vggface,
        "/apdcephfs_cq8/share_1367250/zhentaoyu/Driving/00_VASA/00_data/models/pretrain_models/senet50_scratch_weight.pkl",
    )
    return vggface


@torch.no_grad()
def op_eval_faceid_vgg(opt, device="cuda"):
    print("--------------------Start FaceID--------------------")
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize([0], [1])]
    )
    vggface = vggface2(pretrained=True).to(device)
    vggface.eval()
    vggface_mean = (
        torch.tensor([131.0912, 103.8827, 91.4953]).view(1, 3, 1, 1).detach().to(device)
        / 255
    )
    id_scores = []
    if os.path.isdir(opt.save_dir):
        video_paths = find_data_files(opt.save_dir, "*.mp4")
    else:
        video_paths = [line.strip() for line in open(opt.save_dir, "r").readlines()]
        opt.save_dir = os.path.dirname(opt.save_dir)
    assert len(video_paths) > 0

    # source_image_paths = [line.strip() for line in open(opt.source_list, 'r').readlines()]
    source_image_paths = glob.glob(opt.source_imgae_dir + "/*.*")

    #    embedding_sources = {}
    embedding_sources = []
    for source_image_path in tqdm(source_image_paths):
        image_name = os.path.basename(os.path.splitext(source_image_path)[0])
        source_image = Image.open(source_image_path).convert("RGB")

        h, w = source_image.size
        if opt.det_head:
            area = 1.2
            _, _, bboxes_list = align_instance(
                np.array(source_image)[:, :, [2, 1, 0]], maxface=True, ptstype="5"
            )
            x1, y1, ww, hh = bboxes_list[0]
            x2, y2 = x1 + ww, y1 + hh
            ww, hh = (x2 - x1) * area, (y2 - y1) * area
            center = [(x2 + x1) // 2, (y2 + y1) // 2]
            x1 = max(center[0] - ww // 2, 0)
            y1 = max(center[1] - hh // 2, 0)
            x2 = min(center[0] + ww // 2, w)
            y2 = min(center[1] + hh // 2, h)
            bbox = x1, y1, x2, y2
            bbox_s = process_bbox(bbox, expand_radio=0.4, height=h, width=w)
            x1, y1, x2, y2 = bbox_s
        else:
            x1, y1, x2, y2 = 0, 0, w, h
        source_image = source_image.crop((x1, y1, x2, y2))
        # source_image.save('crop.png')

        source_data = transform(source_image).unsqueeze(0).to(device)
        source_data_lowres = F.interpolate(
            source_data, (224, 224), mode="bilinear", align_corners=False
        )
        embedding_source = (
            vggface(source_data_lowres - vggface_mean).detach().cpu().numpy()
        )
        embedding_source = (
            embedding_source / np.linalg.norm(embedding_source, axis=1)[:, np.newaxis]
        )
        embedding_sources.append(embedding_source)
    embedding_sources = np.concatenate(embedding_sources, axis=0)
    for video_path in tqdm(video_paths):
        # print(video_path)
        video_name = os.path.basename(os.path.splitext(video_path)[0])
        source_name = video_name[:5]
        source_name = video_name[-5:]
        dataset = HumanTalkingVideoDataset(video_path, transform, opt.det_head)
        dataloader = DataLoader(
            dataset,
            batch_size=opt.batch_size,
            num_workers=opt.num_workers,
            shuffle=False,
        )
        for data in dataloader:
            data = data.to(device)
            n, c, h, w = data.shape
            generate_data = data
            generate_data_lowres = F.interpolate(
                generate_data, (224, 224), mode="bilinear", align_corners=False
            )
            embedding_generate = (
                vggface(generate_data_lowres - vggface_mean).detach().cpu().numpy()
            )
            embedding_generate = (
                embedding_generate
                / np.linalg.norm(embedding_generate, axis=1)[:, np.newaxis]
            )
            id_score = np.dot(embedding_sources, embedding_generate.T).max(axis=0)
            id_scores.append(id_score)
    id_scores = np.concatenate(id_scores, axis=0)
    mean_id_score = np.mean(id_scores)
    print("Eval Results:", opt.save_dir)
    print("Face Similarity: %.3f" % mean_id_score)
    f_w = open(os.path.join(opt.save_dir, "eval.txt"), "a")
    f_w.write("VGGFace Similarity: %.3f\n" % mean_id_score)
    f_w.flush()
    f_w.close()
    print("--------------------End FaceID--------------------")


@torch.no_grad()
def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--save_dir", default="./results/", help="path to save result videos and images"
    )
    parser.add_argument("--batch_size", default=16, type=int)
    parser.add_argument("--num_workers", default=8, type=int)
    parser.add_argument("--source_imgae_dir", default="", type=str)
    parser.add_argument("--det_head", action="store_true")

    opt = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    op_eval_faceid_vgg(opt, device)


def run_face_id(image_path):
    try:
        image = Image.open(image_path)
        image = np.asarray(image)[:, :, ::-1]
        h, w, c = image.shape
        source_image = image[:, :h]
        driven_image = image[:, h : h * 2]
        generate_image = image[:, h * 2 :]
        embedding_generate = np.asarray(
            DeepFace.represent(generate_image)[0]["embedding"]
        )
        embedding_source = np.asarray(DeepFace.represent(source_image)[0]["embedding"])
        id_score = embedding_generate.dot(embedding_source)
        return id_score
    except:
        return None


if __name__ == "__main__":
    main()
