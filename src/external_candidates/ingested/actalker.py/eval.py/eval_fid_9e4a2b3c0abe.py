# Extracted from: C:\DEV\PyAgent\.external\ACTalker\eval\eval_fid.py
import fnmatch
import multiprocessing
import os
from argparse import ArgumentParser

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from decord import VideoReader

# from insightface.app import FaceAnalysis
from deepface import DeepFace
from inception import InceptionV3

# from eval import HumanTalkingJsonDataset
from PIL import Image
from scipy import linalg
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


class HumanTalkingImageDataset(Dataset):
    def __init__(
        self,
        image_paths,
        transform,
    ):
        super().__init__()
        self.image_paths = image_paths[:]
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        image = Image.open(image_path)
        image = np.asarray(image)
        pil_image = Image.fromarray(image.astype(np.uint8))
        tensor_image = self.transform(pil_image)
        return tensor_image


def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):
    """Numpy implementation of the Frechet Distance.
    The Frechet distance between two multivariate Gaussians X_1 ~ N(mu_1, C_1)
    and X_2 ~ N(mu_2, C_2) is
            d^2 = ||mu_1 - mu_2||^2 + Tr(C_1 + C_2 - 2*sqrt(C_1*C_2)).

    Stable version by Dougal J. Sutherland.

    Params:
    -- mu1   : Numpy array containing the activations of a layer of the
               inception net (like returned by the function 'get_predictions')
               for generated samples.
    -- mu2   : The sample mean over activations, precalculated on an
               representative data set.
    -- sigma1: The covariance matrix over activations for generated samples.
    -- sigma2: The covariance matrix over activations, precalculated on an
               representative data set.

    Returns:
    --   : The Frechet Distance.
    """

    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)

    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    assert (
        mu1.shape == mu2.shape
    ), "Training and test mean vectors have different lengths"
    assert (
        sigma1.shape == sigma2.shape
    ), "Training and test covariances have different dimensions"

    diff = mu1 - mu2

    # Product might be almost singular
    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    if not np.isfinite(covmean).all():
        msg = (
            "fid calculation produces singular product; "
            "adding %s to diagonal of cov estimates"
        ) % eps
        print(msg)
        offset = np.eye(sigma1.shape[0]) * eps
        covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

    # Numerical error might give slight imaginary component
    if np.iscomplexobj(covmean):
        if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
            m = np.max(np.abs(covmean.imag))
            raise ValueError("Imaginary component {}".format(m))
        covmean = covmean.real

    tr_covmean = np.trace(covmean)

    return diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean


def find_data_files(directory, prefix):
    mp4_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, prefix):
            mp4_files.append(os.path.join(root, filename))
    return mp4_files


@torch.no_grad()
def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--save_dir", default="./results/", help="path to save result videos and images"
    )
    parser.add_argument("--dims", default=2048)
    parser.add_argument("--model_path", default=None)
    parser.add_argument("--batch_size", default=16, type=int)
    parser.add_argument("--num_workers", default=8, type=int)
    parser.add_argument("--fid", action="store_true")
    parser.add_argument("--faceid", action="store_true")

    opt = parser.parse_args()
    if opt.model_path is not None:
        model_name = os.path.splitext(os.path.basename(opt.model_path))[0]
        opt.save_dir = os.path.join(opt.save_dir, model_name)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载 inception 模型
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[opt.dims]
    inception_model = InceptionV3([block_idx]).to(device)
    inception_model.eval()

    # 定义数据集和数据加载器
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize([0], [1])]
    )

    image_paths = find_data_files(opt.save_dir, "*.png")
    if opt.fid:
        op_eval_fid(opt, image_paths, inception_model, transform, device)

    if opt.faceid:
        op_eval_faceid(opt, image_paths)


def run_face_id(image_path):
    try:
        image = Image.open(image_path)
        image = np.asarray(image)[:, :, ::-1]
        h, w, c = image.shape
        source_image = image[:, :h]
        # driven_image = image[:, h:h*2]
        # generate_image = image[:, h*2:]
        generate_image = image[:, w // 2 :]
        embedding_generate = np.asarray(
            DeepFace.represent(generate_image)[0]["embedding"]
        )
        embedding_source = np.asarray(DeepFace.represent(source_image)[0]["embedding"])
        id_score = embedding_generate.dot(embedding_source)
        return id_score
    except:
        return None


def op_eval_faceid(opt, image_paths):
    # face_detector = FaceAnalysis(providers=['CUDAExecutionProvider'])
    # face_detector.prepare(ctx_id=0, det_size=(640, 640))
    print("--------------------Start FaceID--------------------")
    scores = [0.0, 0]
    pool = multiprocessing.Pool(5)
    results = []
    for image_path in tqdm(image_paths):
        results.append(pool.apply_async(run_face_id, args=(image_path,)))
    pool.close()
    for result in tqdm(results):
        score = result.get()
        if score is not None:
            scores[0] += score
            scores[1] += 1
    pool.join()
    mean_id_score = scores[0] / scores[1]
    print("Eval Results:", opt.save_dir)
    print("Face Similarity: %.3f" % mean_id_score)
    f_w = open(os.path.join(opt.save_dir, "eval.txt"), "a")
    f_w.write("Face Similarity: %.3f\n" % mean_id_score)
    f_w.flush()
    f_w.close()
    print("--------------------End FaceID--------------------")


def op_eval_fid(opt, image_paths, inception_model, transform, device):
    features1 = []
    features2 = []

    dataset = HumanTalkingImageDataset(image_paths, transform)
    dataloader = DataLoader(
        dataset, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=False
    )
    print("--------------------Start FID--------------------")
    for data in tqdm(dataloader):
        data = data.to(device)
        n, c, h, w = data.shape
        length = w // 3
        driven_data = data[..., length * 1 : length * 2]
        generate_data = data[..., length * 2 : length * 3]
        features1.append(
            inception_model(driven_data)[0].squeeze(-1).squeeze(-1).cpu().numpy()
        )
        features2.append(
            inception_model(generate_data)[0].squeeze(-1).squeeze(-1).cpu().numpy()
        )

    features1 = np.concatenate(features1, axis=0)
    features2 = np.concatenate(features2, axis=0)

    # 计算 FID
    mu1 = np.mean(features1, axis=0)
    mu2 = np.mean(features2, axis=0)

    sigma1 = np.cov(features1, rowvar=False)
    sigma2 = np.cov(features2, rowvar=False)

    fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
    print("Eval Results:", opt.save_dir)
    print("FID: %.3f" % fid)
    print("--------------------End FID--------------------")
    f_w = open(os.path.join(opt.save_dir, "eval.txt"), "a")
    f_w.write("FID: %.3f\n" % fid)
    f_w.flush()
    f_w.close()
    print()


# def cal_cross_video(opt, video_paths, model, transform, device):
#     features1 = []
#     features2 = []
#     for video_path in tqdm(video_paths):
#         driven_video = HumanTalkingVideoDataset(video_path, transform, 1)
#         driven_video_loader = DataLoader(driven_video, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=False)
#         generate_video = HumanTalkingVideoDataset(video_path, transform, 2)
#         generate_video_loader = DataLoader(generate_video, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=False)

#         for data in driven_video_loader:
#             # features1.append(model(data.unsqueeze(0).to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())
#             features1.append(model(data.to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())

#         # for index in range(len(driven_video)):
#         for data in generate_video_loader:
#             # features2.append(model(data.unsqueeze(0).to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())
#             features2.append(model(data.to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())

#     features1 = np.concatenate(features1, axis=0)
#     features2 = np.concatenate(features2, axis=0)

#     # 计算 FID
#     mu1 = np.mean(features1, axis=0)
#     mu2 = np.mean(features2, axis=0)

#     sigma1 = np.cov(features1, rowvar=False)
#     sigma2 = np.cov(features2, rowvar=False)

#     fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
#     print('Eval Results:', opt.save_dir)
#     print('FID: %.3f' % fid)
#     print('--------------------end--------------------')
#     print()

# cal_same_video(opt, driven_video_paths, model, transform)
# def cal_same_video(opt, driven_video_paths, model, transform, device='cuda'):
#     total_fid = [0.0, 0]
#     for driven_video_path in tqdm(driven_video_paths):
#         features1 = []
#         features2 = []
#         video_name = os.path.splitext('/'.join(driven_video_path.split('/')[-name_prefix:]))[0] + '.mp4'
#         save_video_path = os.path.join(opt.save_dir, video_name)
#         driven_video = HumanTalkingJsonDataset(driven_video_path, transform)
#         driven_video_loader = DataLoader(driven_video, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=False)
#         generate_video = HumanTalkingVideoDataset(save_video_path, transform)
#         generate_video_loader = DataLoader(generate_video, batch_size=opt.batch_size, num_workers=opt.num_workers, shuffle=False)

#         for data in driven_video:
#             features1.append(model(data[0].unsqueeze(0).to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())
#             total_index += 1

#         for index in range(len(driven_video)):
#             features2.append(model(generate_video[index].unsqueeze(0).to(device))[0].squeeze(-1).squeeze(-1).cpu().numpy())
#             total_index += 1

#         features1 = np.concatenate(features1, axis=0)
#         features2 = np.concatenate(features2, axis=0)

#         # 计算 FID
#         mu1 = np.mean(features1, axis=0)
#         mu2 = np.mean(features2, axis=0)

#         sigma1 = np.cov(features1, rowvar=False)
#         sigma2 = np.cov(features2, rowvar=False)

#         fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
#         total_fid[0] += fid
#         total_fid[1] += 1
#     fid = total_fid[0] / total_fid[1]
#     print('Eval Results:', opt.save_dir)
#     print('FID: %.3f' % fid)


if __name__ == "__main__":
    main()


# 定义 VGG 模型
# class VGGFeatures(nn.Module):
#     def __init__(self):
#         super(VGGFeatures, self).__init__()
#         vgg = models.vgg19(pretrained=True)
#         self.features = nn.Sequential(*list(vgg.features.children())[:44])

#     def forward(self, x):
#         return self.features(x)


# # 定义计算 FID 的函数
# def calculate_fid(dataset1_path, dataset2_path, batch_size=32, num_workers=4):
#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     # 加载 VGG 模型
#     vgg = VGGFeatures().to(device)
#     vgg.eval()

#     # 定义数据集和数据加载器
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#     ])

#     dataset1 = CustomDataset(dataset1_path, transform=transform)
#     dataset2 = CustomDataset(dataset2_path, transform=transform)

#     data_loader1 = DataLoader(dataset1, batch_size=batch_size, num_workers=num_workers, shuffle=False)
#     data_loader2 = DataLoader(dataset2, batch_size=batch_size, num_workers=num_workers, shuffle=False)

#     # 提取特征
#     features1 = []
#     features2 = []

#     with torch.no_grad():
#         for images in data_loader1:
#             images = images.to(device)
#             features1.append(vgg(images).cpu().numpy())

#         for images in data_loader2:
#             images = images.to(device)
#             features2.append(vgg(images).cpu().numpy())

#     features1 = np.concatenate(features1, axis=0)
#     features2 = np.concatenate(features2, axis=0)

#     # 计算 FID
#     mu1 = np.mean(features1, axis=0)
#     mu2 = np.mean(features2, axis=0)

#     sigma1 = np.cov(features1, rowvar=False)
#     sigma2 = np.cov(features2, rowvar=False)

#     fid = calculate_frechet_distance(mu1, sigma1, mu2, sigma2)

#     return fid


# class HumanTalkingVideoDataset(Dataset):
#     def __init__(
#         self,
#         video_path,
#         transform,
#         start
#     ):
#         super().__init__()
#         self.video_path = video_path
#         self.video_reader = VideoReader(self.video_path)
#         self.fps = int(round(self.video_reader.get_avg_fps()))
#         self.video_length = len(self.video_reader)
#         self.transform = transform
#         self.start = start

#     def __len__(self):
#         return self.video_length

#     def __getitem__(self, index):
#         video_reader = VideoReader(self.video_path)
#         image = video_reader[index].asnumpy()
#         h, w = image.shape[:2]
#         image = image[:, self.start * h: self.start * h + h]
#         pil_image = Image.fromarray(image.astype(np.uint8))
#         tensor_image = self.transform(pil_image)
#         return tensor_image
