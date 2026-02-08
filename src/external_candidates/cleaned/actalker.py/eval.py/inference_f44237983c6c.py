# Extracted from: C:\DEV\PyAgent\.external\ACTalker\eval\inference.py
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from modules.dataloader.stage_one_dataloader import HumanTalkingJsonDataset
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
import json
from argparse import ArgumentParser

import yaml
from decord import VideoReader
from deepface import DeepFace
from modules.model.base_model import (
    Discriminator_cycle,
    Discriminator_patch,
    HeadPose_train,
)
from modules.model.generator import Generator, Generator_old

# from insightface.app import FaceAnalysis
from modules.util import center_crop
from moviepy.editor import ImageSequenceClip, VideoFileClip
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

name_prefix = 3


def create_instance_by_name(class_name: str):
    # 使用globals()获取全局命名空间中的所有定义
    class_defs = globals()

    # 使用getattr()根据字符串名称获取对应的类
    class_def = class_defs.get(class_name)

    # 检查是否找到了对应的类
    if class_def is None or not isinstance(class_def, type):
        raise ValueError(f"No such class: {class_name}")

    # 创建类的实例
    # instance = class_def()
    return class_def


@torch.no_grad()
def driven_video(
    opt,
    generator,
    pose_model,
    transform,
    source_image_path,
    driven_video_path,
    save_path,
):
    device = generator.device
    video_data = HumanTalkingJsonDataset(driven_video_path, transform)
    generate_image_loader = DataLoader(video_data, batch_size=opt.batch_size, num_workers=1, shuffle=False)
    if source_image_path is not None:
        # face_detector = FaceAnalysis(providers=['CUDAExecutionProvider'])
        # face_detector.prepare(ctx_id=0, det_size=(640, 640))
        # faces = face_detector.get(source_image)
        source_image = cv2.imread(source_image_path)
        faces = DeepFace.analyze(source_image[:, :, ::-1], actions=["emotion"], enforce_detection=False)

        facial_area = faces[0]["region"]
        face_bbox = [
            facial_area["x"],
            facial_area["y"],
            facial_area["w"],
            facial_area["h"],
        ]
        face_bbox[2] += face_bbox[0]
        face_bbox[3] += face_bbox[1]
        source_face_image, _ = center_crop(source_image, face_bbox)

        source_image = cv2.resize(source_image, (256, 256))
        source_image_pil = Image.fromarray(source_image[:, :, ::-1])
        source_image_tensor = transform(source_image_pil)

        source_face_image = cv2.resize(source_face_image, (256, 256))
        source_face_image_pil = Image.fromarray(source_face_image[:, :, ::-1])
        source_face_image_tensor = transform(source_face_image_pil)
        # source_mask_tensor = torch.ones_like(source_image_tensor)
        # source_background_tensor = torch.zeros_like(source_image_tensor)
    else:
        source_image_tensor, source_face_image_tensor, _, _ = video_data[0]
    source_image = (source_image_tensor.clone().permute((1, 2, 0)).numpy() * 255).astype(np.uint8)[:, :, ::-1]

    source_image_tensor = source_image_tensor.to(device).unsqueeze(0)
    source_face_image_tensor = source_face_image_tensor.to(device).unsqueeze(0)
    source_pose = pose_model(source_image_tensor * 2 - 1)
    vs, global_descriptor, _ = generator.extract_feature(source_image_tensor, source_face_image_tensor, source_pose)

    save_paths = []
    index = 0
    for data in generate_image_loader:
        driven_images_tensor, driven_face_images_tensor, _, _ = data
        # driven_images_tensor = torch.cat([torch.zeros_like(driven_images_tensor)[:, :, :, -60:], driven_images_tensor[:, :, :, :-60]], dim=-1)
        # driven_images_tensor = torch.cat([torch.zeros_like(driven_images_tensor)[:, :, -30:, :], driven_images_tensor[:, :, :-30, :]], dim=-2)
        n, c, h, w = driven_images_tensor.shape
        driven_images = (driven_images_tensor.clone().permute((0, 2, 3, 1)).numpy() * 255).astype(np.uint8)[
            :, :, :, ::-1
        ]
        driven_images_tensor = driven_images_tensor.to(device)
        driven_face_images_tensor = driven_face_images_tensor.to(device)
        driven_pose = pose_model(driven_images_tensor * 2 - 1)
        vs_batch = vs.clone().repeat((n, 1, 1, 1, 1))
        global_descriptor_batch = global_descriptor.clone().repeat((n, 1))
        output = generator.drive_feature(vs_batch, global_descriptor_batch, driven_face_images_tensor, driven_pose)
        # output = generator.drive_feature(vs_batch, global_descriptor_batch, driven_face_images_tensor, source_pose)

        output_images = (
            (output.permute((0, 2, 3, 1)).cpu().detach().numpy() * 255).clip(0, 255).astype(np.uint8)[:, :, :, ::-1]
        )

        for ii in range(len(output_images)):
            output_image = output_images[ii]
            driven_image = driven_images[ii]
            img = np.concatenate([source_image, driven_image, output_image], axis=1)
            img_path = os.path.join(os.path.splitext(save_path)[0], "%05d.png" % index)
            index += 1
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            cv2.imwrite(img_path, img)
            save_paths.append(img_path)
    del generate_image_loader
    video_clip = VideoFileClip(video_data.video_path)
    audio_clip = video_clip.audio

    clip = ImageSequenceClip(save_paths, fps=video_data.fps)
    clip = clip.set_duration(video_clip.duration)
    clip = clip.set_audio(audio_clip)
    clip.write_videofile(save_path, codec="libx264", audio_codec="mp3")


def main():
    parser = ArgumentParser()
    parser.add_argument("--config", default="config/train-stage1.yaml", help="path to config")
    parser.add_argument("--source_image_list", default=None, help="source img or json")
    parser.add_argument("--batch_size", default=16, type=int)
    parser.add_argument("--num", default=-1, type=int)
    parser.add_argument("--video_list", default="", help="json list of driven video")
    parser.add_argument("--save_dir", default="./results/", help="path to save result videos and images")
    parser.add_argument("--model_path", default=None)
    parser.add_argument("--mode", default="self")

    opt = parser.parse_args()
    with open(opt.config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    device = "cuda"
    img_size = config["dataset_params"]["img_size"]
    transform = transforms.Compose(
        [
            transforms.Resize(img_size),
            transforms.ToTensor(),
            transforms.Normalize([0], [1]),
        ]
    )

    out_dir = os.path.join(opt.save_dir, os.path.splitext(os.path.basename(opt.model_path))[0])
    checkpoint = torch.load(opt.model_path, map_location="cpu")

    pose_model = HeadPose_train().to(device)
    generator = create_instance_by_name(config["model_params"]["common_params"]["generator_type"])(config, device)
    generator_data = checkpoint["generator"]
    new_generator_data = {}
    for key in generator_data.keys():
        if key[:7] == "module.":
            new_generator_data[key[7:]] = generator_data[key]
        else:
            new_generator_data[key] = generator_data[key]
    generator.load_state_dict(new_generator_data)
    pose_model.load_state_dict(checkpoint["pose_model"])
    generator.eval()
    pose_model.eval()
    source_image_paths = [line.strip() for line in open(opt.source_image_list, "r").readlines()]
    driven_video_paths = [line.strip() for line in open(opt.video_list, "r").readlines()]
    if opt.num > 0:
        driven_video_paths = driven_video_paths[: opt.num]
    for index, driven_video_path in tqdm(enumerate(driven_video_paths[:])):
        video_name = os.path.splitext("/".join(driven_video_path.split("/")[-name_prefix:]))[0] + ".mp4"
        save_video_path = os.path.join(out_dir, video_name)
        # if os.path.exists(save_video_path):
        #     continue
        if opt.mode == "cross":
            driven_video(
                opt,
                generator,
                pose_model,
                transform,
                source_image_paths[index],
                driven_video_path,
                save_video_path,
            )
        elif opt.mode == "self":
            driven_video(
                opt,
                generator,
                pose_model,
                transform,
                None,
                driven_video_path,
                save_video_path,
            )
        else:
            raise NotImplemented


if __name__ == "__main__":
    main()


# class HumanTalkingJsonImageDataset(Dataset):
#     def __init__(
#         self,
#         data_meta_path,
#         transform,
#     ):
#         super().__init__()
#         self.transform = transform
#         data = json.load(open(data_meta_path, 'r'))
#         self.video_path = data['mp4_path']
#         self.fps = int(data['fps'])
#         self.relocate_dir = '/apdcephfs_cq5/share_300167803/zhentaoyu/DATA/public/voxceleb2/official/test/img'
#         video_name = os.path.splitext('/'.join(self.video_path.split('/')[-name_prefix:]))[0]
#         video_dir = os.path.join(self.relocate_dir, video_name)
#         self.image_paths = []
#         for file_name in os.listdir(video_dir):
#             if '.png' in file_name:
#                 self.image_paths.append(os.path.join(video_dir, file_name))
#         self.image_paths = sorted(self.image_paths)

#     def __len__(self):
#         return len(self.image_paths)

#     def __getitem__(self, index):
#         pil_image = Image.open(self.image_paths[index])
#         tensor_image = self.transform(pil_image)
#         empty_image = torch.ones_like(tensor_image)
#         mask  = torch.ones_like(tensor_image)
#         return tensor_image, mask, empty_image
