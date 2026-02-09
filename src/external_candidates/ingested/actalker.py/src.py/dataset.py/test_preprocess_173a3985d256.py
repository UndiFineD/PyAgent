# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\dataset\test_preprocess.py
import copy
import os
import pdb

# from .portrait_audio_dataset import process_bbox, get_bbox_by_aspect  # Commented out - using functions from portrait_audio_dataset_arcface_vasa instead
import cv2
import decord
import librosa
import mediapipe as mp
import numpy as np
import torch
import torchvision.transforms as transforms
import tqdm
from PIL import Image
from transformers import AutoFeatureExtractor, CLIPImageProcessor

from src.utils.face_align import AlignImage
from src.utils.mediapipe.mp_utils_refine import LMKExtractor

from .portrait_audio_dataset_arcface_vasa import (
    align_face,
    center_crop,
    draw_pose,
    get_bbox_by_aspect,
    process_bbox,
)

mean_face_lm5p = np.array(
    [
        [(30.2946 + 8) * 2 + 16, 51.6963 * 2],  # left eye pupil
        [(65.5318 + 8) * 2 + 16, 51.5014 * 2],  # right eye pupil
        [(48.0252 + 8) * 2 + 16, 71.7366 * 2],  # nose tip
        [(33.5493 + 8) * 2 + 16, 92.3655 * 2],  # left mouth corner
        [(62.7299 + 8) * 2 + 16, 92.2041 * 2],  # right mouth corner
    ],
    dtype=np.float32,
)
DEFAULT_CROP_SIZE = [512, 512]

device_id = 0
device = "cuda:{}".format(device_id) if device_id > -1 else "cpu"
# Note: These paths should be configurable through config file
# For now using default paths, consider refactoring to use config
BASE_DIR = "enhance_model/yt_align/"
det_path = os.path.join(BASE_DIR, "yoloface_v5l.pt")
p1_path = os.path.join(BASE_DIR, "p1.pt")
p2_path = os.path.join(BASE_DIR, "p2.pt")

# Initialize AlignImage only if model files exist
align_instance = None
if os.path.exists(det_path) and os.path.exists(p1_path) and os.path.exists(p2_path):
    try:
        align_instance = AlignImage(
            device, det_path=det_path, p1_path=p1_path, p2_path=p2_path
        )
        print("✓ Face alignment models loaded successfully")
    except Exception as e:
        print(f"⚠️ Failed to load face alignment models: {e}")
        align_instance = None
else:
    print("⚠️ Face alignment model files not found, face alignment will be disabled")
    print(
        f"   Missing files: det_path={det_path}, p1_path={p1_path}, p2_path={p2_path}"
    )
    align_instance = None
mediapipe_align_instance = LMKExtractor()
mp_connections = mp.solutions.face_mesh_connections


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


def get_custom_affine_transform_512(target_face_lm5p):
    mat_warp = np.zeros((2, 3))
    A = np.zeros((4, 4))
    B = np.zeros((4))
    for i in range(5):
        # sa[0][0] += a[i].x*a[i].x + a[i].y*a[i].y;
        A[0][0] += (
            target_face_lm5p[i][0] * target_face_lm5p[i][0]
            + target_face_lm5p[i][1] * target_face_lm5p[i][1]
        )
        # sa[0][2] += a[i].x;
        A[0][2] += target_face_lm5p[i][0]
        # sa[0][3] += a[i].y;
        A[0][3] += target_face_lm5p[i][1]

        # sb[0] += a[i].x*b[i].x + a[i].y*b[i].y;
        B[0] += (
            target_face_lm5p[i][0] * mean_face_lm5p[i][0] * 2
            + target_face_lm5p[i][1] * mean_face_lm5p[i][1] * 2
        )
        # sb[1] += a[i].x*b[i].y - a[i].y*b[i].x;
        B[1] += (
            target_face_lm5p[i][0] * mean_face_lm5p[i][1] * 2
            - target_face_lm5p[i][1] * mean_face_lm5p[i][0] * 2
        )
        # sb[2] += b[i].x;
        B[2] += mean_face_lm5p[i][0] * 2
        # sb[3] += b[i].y;
        B[3] += mean_face_lm5p[i][1] * 2

    # sa[1][1] = sa[0][0];
    A[1][1] = A[0][0]
    # sa[2][1] = sa[1][2] = -sa[0][3];
    A[2][1] = A[1][2] = -A[0][3]
    # sa[3][1] = sa[1][3] = sa[2][0] = sa[0][2];
    A[3][1] = A[1][3] = A[2][0] = A[0][2]
    # sa[2][2] = sa[3][3] = count;
    A[2][2] = A[3][3] = 5
    # sa[3][0] = sa[0][3];
    A[3][0] = A[0][3]

    _, mat23 = cv2.solve(A, B, flags=cv2.DECOMP_SVD)
    mat_warp[0][0] = mat23[0]
    mat_warp[1][1] = mat23[0]
    mat_warp[0][1] = -mat23[1]
    mat_warp[1][0] = mat23[1]
    mat_warp[0][2] = mat23[2]
    mat_warp[1][2] = mat23[3]

    return mat_warp


def get_audio_feature(audio_path):
    feature_extractor = AutoFeatureExtractor.from_pretrained(
        "enhance_model/whisper-tiny/"
    )
    audio_input, sampling_rate = librosa.load(audio_path, sr=16000)
    assert sampling_rate == 16000

    audio_features = []
    window = 750 * 640
    for i in range(0, len(audio_input), window):
        audio_feature = feature_extractor(
            audio_input[i : i + window],
            sampling_rate=sampling_rate,
            return_tensors="pt",
        ).input_features
        audio_features.append(audio_feature)
    # import ipdb
    # ipdb.set_trace()
    audio_features = torch.cat(audio_features, dim=-1)
    return audio_features, len(audio_input) // 640


def process_image_multires(image_path, expand_ratio=1.0, aspect_type=0, image_size=512):

    imSrc_ = Image.open(image_path).convert("RGB")
    w, h = imSrc_.size

    if align_instance is not None:
        _, _, bboxes_list = align_instance(
            np.array(imSrc_)[:, :, [2, 1, 0]], maxface=True, ptstype="5"
        )
    else:
        # Use default bbox when face alignment is not available
        print("⚠️ Face alignment disabled, using default bounding box")
        bboxes_list = [np.array([0, 0, w, h])]  # Full image bbox

    if len(bboxes_list) > 0:
        bboxSrc = bboxes_list[0]

        x1, y1, ww, hh = bboxSrc
        x2, y2 = x1 + ww, y1 + hh

        bbox = x1, y1, x2, y2
        print("bbox", bbox, bbox[2] - bbox[0], bbox[3] - bbox[1])
        print("expand_ratio: ", expand_ratio)

        bbox_s = process_bbox(bbox, expand_radio=expand_ratio, height=h, width=w)
        print("bbox_s: ", bbox_s, bbox_s[2] - bbox_s[0], bbox_s[3] - bbox_s[1])

        x1, y1, x2, y2 = get_bbox_by_aspect(bbox_s, aspect_type, w, h)
        imSrc_ = imSrc_.crop((x1, y1, x2, y2))

    w, h = imSrc_.size
    scale = image_size / min(w, h)
    new_w = round(w * scale / 64) * 64
    new_h = round(h * scale / 64) * 64
    imSrc = imSrc_.resize((new_w, new_h), Image.LANCZOS)

    return imSrc


def crop_resize_img(img, bbox, image_size):
    x1, y1, x2, y2 = bbox
    img = img.crop((x1, y1, x2, y2))
    w, h = img.size
    # assert w==h
    img = img.resize((image_size, image_size))
    return img


vasa_image_size = 256
vasa_transform = transforms.Compose(
    [
        transforms.Resize(vasa_image_size),
        transforms.ToTensor(),
        transforms.Normalize([0], [1]),
    ]
)


def crop_face_vasa(image, landmark):
    face_landmark = np.asarray(landmark[:174])
    face_x_min, face_x_max = min(face_landmark[:, 0]), max(face_landmark[:, 0])
    face_y_min, face_y_max = min(face_landmark[:, 1]), max(face_landmark[:, 1])
    lmk_face_bbox = np.asarray([face_x_min, face_y_min, face_x_max, face_y_max])
    vasa_crop_face = center_crop(image, lmk_face_bbox)
    vasa_crop_face = Image.fromarray(vasa_crop_face)
    vasa_crop_face_tensor = vasa_transform(vasa_crop_face)
    return vasa_crop_face_tensor


def preprocess_resize_shortedge(
    image_path,
    audio_path,
    video_path=None,
    pose_path=None,
    limit=100,
    image_size=512,
    area=1.25,
    crop=None,
    expand_ratio=1.0,
    enhance_instance=None,
    aspect_type="1:1",
    with_id_encoder=False,
):

    clip_processor = CLIPImageProcessor()

    to_tensor = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    pose_to_tensor = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )
    indices = get_semantic_indices()

    imSrc_ = Image.open(image_path).convert("RGB")
    w, h = imSrc_.size

    if align_instance is not None:
        _, _, bboxes_list = align_instance(
            np.array(imSrc_)[:, :, [2, 1, 0]], maxface=True, ptstype="5"
        )
        bboxSrc = bboxes_list[0]
    else:
        # Use default bbox when face alignment is not available
        print("⚠️ Face alignment disabled, using full image as bbox")
        bboxSrc = np.array([0, 0, w, h])
    # mediapipe_landmark = mediapipe_align_instance(cv2.imread(image_path))
    # mouth_landmark = mediapipe_landmark['lmks'][indices['Lips']]
    # """ 获得嘴部mask图片 """
    # mouth_mask_array = np.zeros_like(np.array(imSrc_))
    # max_x = max(mouth_landmark[:, 0])*imSrc_.width
    # max_y = max(mouth_landmark[:, 1])*imSrc_.height
    # min_x = min(mouth_landmark[:, 0])*imSrc_.width
    # min_y = min(mouth_landmark[:, 1])*imSrc_.height
    # ww, hh = (max_x-min_x)*2, (max_y-min_y)*2
    # center = [(max_x+min_x)//2, (max_y+min_y)//2]
    # x1 = max(center[0] - ww//2, 0)
    # y1 = max(center[1] - hh//2, 0)
    # x2 = min(center[0] + ww//2, w)
    # y2 = min(center[1] + hh//2, h)
    # mouth_mask_array[int(y1):int(y2), int(x1):int(x2)] = 255
    # mouth_mask = Image.fromarray(mouth_mask_array)

    """ 获得头部图片 """
    if with_id_encoder:
        x1, y1, ww, hh = bboxSrc
        x2, y2 = x1 + ww, y1 + hh
        head_img = imSrc_.crop((x1, y1, x2, y2))
    """ 获得头部图片 """

    pose_img_array = np.zeros_like(np.array(imSrc_))
    x1, y1, ww, hh = bboxSrc
    x2, y2 = x1 + ww, y1 + hh
    ww, hh = (x2 - x1) * area, (y2 - y1) * area
    center = [(x2 + x1) // 2, (y2 + y1) // 2]
    x1 = max(center[0] - ww // 2, 0)
    y1 = max(center[1] - hh // 2, 0)
    x2 = min(center[0] + ww // 2, w)
    y2 = min(center[1] + hh // 2, h)
    pose_img_array[int(y1) : int(y2), int(x1) : int(x2)] = 255
    pose_img = Image.fromarray(pose_img_array)

    mouth_mask_array = np.zeros_like(np.array(imSrc_))
    mouth_mask_array[(int(y1) + int(y2) // 2) : int(y2), int(x1) : int(x2)] = 255
    mouth_mask = Image.fromarray(mouth_mask_array)

    exp_mask_array = pose_img_array - mouth_mask_array
    exp_mask = Image.fromarray(exp_mask_array)

    if crop:
        bbox = x1, y1, x2, y2
        print("expand_ratio: ", expand_ratio)
        bbox_s = process_bbox(bbox, expand_radio=expand_ratio, height=h, width=w)
        x1, y1, x2, y2 = get_bbox_by_aspect(bbox_s, aspect_type, w, h)
        imSrc_ = imSrc_.crop((x1, y1, x2, y2))
        pose_img = pose_img.crop((x1, y1, x2, y2))
        exp_mask = exp_mask.crop((x1, y1, x2, y2))
        mouth_mask = mouth_mask.crop((x1, y1, x2, y2))
    w, h = imSrc_.size
    scale = image_size / min(w, h)
    new_w = round(w * scale / 64) * 64
    new_h = round(h * scale / 64) * 64
    imSrc = imSrc_.resize((new_w, new_h), Image.LANCZOS)
    pose_img = pose_img.resize((new_w, new_h), Image.LANCZOS)
    exp_mask = exp_mask.resize((new_w, new_h), Image.LANCZOS)
    mouth_mask = mouth_mask.resize((new_w, new_h), Image.LANCZOS)
    if enhance_instance is not None:
        print("enhance image")
        bgr_in = np.array(imSrc)[:, :, [2, 1, 0]]
        bgr_in = bgr_in.round().astype(np.uint8).copy()
        h, w = bgr_in.shape[:2]
        if align_instance is not None:
            pts5_list, _, _ = align_instance(bgr_in, maxface=True, ptstype="5")
        else:
            # Use default face landmarks when face alignment is not available
            pts5_list = [
                np.array(
                    [
                        [w * 0.3, h * 0.4],
                        [w * 0.7, h * 0.4],
                        [w * 0.5, h * 0.5],
                        [w * 0.35, h * 0.7],
                        [w * 0.65, h * 0.7],
                    ]
                )
            ]
        warp_mat = get_custom_affine_transform_512(pts5_list[0])
        enhance_crop_bgr = cv2.warpAffine(
            bgr_in, warp_mat, (512, 512), flags=cv2.INTER_CUBIC
        )
        enhance_out = enhance_instance.enhance_cropface(enhance_crop_bgr)
        bgr_out = copy.deepcopy(bgr_in)
        bgr_out = cv2.warpAffine(
            enhance_out,
            warp_mat,
            (w, h),
            dst=bgr_out,
            flags=(cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP),
            borderMode=cv2.BORDER_TRANSPARENT,
        )
        bgr_out = (
            ((bgr_in.astype(np.float) + bgr_out.astype(np.float)) / 2.0)
            .round()
            .astype(np.uint8)
        )
        imSrc = Image.fromarray(bgr_out[:, :, [2, 1, 0]])
    # pose_img.save('pose_img.png')
    # imSrc.save('imSrc.png')

    clip_image = clip_processor(
        images=imSrc.resize((224, 224), Image.LANCZOS), return_tensors="pt"
    ).pixel_values[0]
    audio_input, audio_len = get_audio_feature(audio_path)

    audio_len = min(limit, audio_len)
    if video_path:
        if not pose_path:
            pose_path = video_path
        if video_path.endswith(".mp4"):
            cap = decord.VideoReader(video_path, fault_tol=1)
            total_frames = min(len(cap), limit)
            driven_face_images_list = []
            driven_pose_images_list = []
            # driven_dwpose_images_list = []
            driven_expression_tensor_list = []
            landmark = None
            bbox_s = None
            for drive_idx in tqdm.tqdm(range(total_frames), ncols=0):
                frame = cap[drive_idx].asnumpy()
                ytpts_list, scores_list, bboxes_list = align_instance(
                    frame[:, :, [2, 1, 0]]
                )
                if len(ytpts_list) > 0:
                    landmark = ytpts_list[0]
                assert landmark is not None

                if bbox_s is None:
                    x1, y1, ww, hh = bboxes_list[0]
                    x2, y2 = x1 + ww, y1 + hh
                    bbox = [x1, y1, x2, y2]
                    bbox_s = process_bbox(
                        bbox,
                        expand_radio=1,
                        height=frame.shape[0],
                        width=frame.shape[1],
                    )

                driven_face_images_tensor = crop_face_vasa(frame.copy(), landmark)
                driven_face_images_list.append(driven_face_images_tensor)
                driven_image = Image.fromarray(frame)
                driven_image = crop_resize_img(driven_image, bbox_s, image_size)
                driven_image_tensor = to_tensor(driven_image)
                driven_expression_tensor_list.append(driven_image_tensor)
        else:
            driven_face_images_list = []
            driven_pose_images_list = []
            # driven_dwpose_images_list = []
            driven_expression_tensor_list = []
            landmark = None
            bbox_s = None
            frame = cv2.imread(video_path)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ytpts_list, scores_list, bboxes_list = align_instance(
                frame[:, :, [2, 1, 0]]
            )
            if len(ytpts_list) > 0:
                landmark = ytpts_list[0]
            assert landmark is not None

            if bbox_s is None:
                x1, y1, ww, hh = bboxes_list[0]
                x2, y2 = x1 + ww, y1 + hh
                bbox = [x1, y1, x2, y2]
                bbox_s = process_bbox(
                    bbox, expand_radio=1, height=frame.shape[0], width=frame.shape[1]
                )

            driven_face_images_tensor = crop_face_vasa(frame.copy(), landmark)
            driven_face_images_list.append(driven_face_images_tensor)
            driven_image = Image.fromarray(frame)
            driven_image = crop_resize_img(driven_image, bbox_s, image_size)
            driven_image_tensor = to_tensor(driven_image)
            driven_expression_tensor_list.append(driven_image_tensor)

        if pose_path.endswith(".mp4"):
            cap = decord.VideoReader(pose_path, fault_tol=1)
            total_frames = min(len(cap), limit)
            driven_pose_images_list = []
            driven_pose_tensor_list = []
            landmark = None
            bbox_s = None
            for drive_idx in tqdm.tqdm(range(total_frames), ncols=0):
                frame = cap[drive_idx].asnumpy()
                ytpts_list, scores_list, bboxes_list = align_instance(
                    frame[:, :, [2, 1, 0]]
                )
                if len(ytpts_list) > 0:
                    landmark = ytpts_list[0]
                assert landmark is not None

                if bbox_s is None:
                    x1, y1, ww, hh = bboxes_list[0]
                    x2, y2 = x1 + ww, y1 + hh
                    bbox = [x1, y1, x2, y2]
                    bbox_s = process_bbox(
                        bbox,
                        expand_radio=1,
                        height=frame.shape[0],
                        width=frame.shape[1],
                    )

                driven_pose_image = Image.fromarray(frame)
                driven_pose_image = crop_resize_img(
                    driven_pose_image, bbox_s, image_size
                )
                driven_pose_images_tensor = vasa_transform(
                    driven_pose_image
                )  # 3, 256, 256
                driven_pose_images_list.append(driven_pose_images_tensor)
                driven_image_tensor = to_tensor(driven_pose_image)
                driven_pose_tensor_list.append(driven_image_tensor)
        else:
            driven_pose_images_list = []
            driven_pose_tensor_list = []
            landmark = None
            bbox_s = None
            frame = cv2.imread(pose_path).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ytpts_list, scores_list, bboxes_list = align_instance(
                frame[:, :, [2, 1, 0]]
            )
            if len(ytpts_list) > 0:
                landmark = ytpts_list[0]
            assert landmark is not None

            if bbox_s is None:
                x1, y1, ww, hh = bboxes_list[0]
                x2, y2 = x1 + ww, y1 + hh
                bbox = [x1, y1, x2, y2]
                bbox_s = process_bbox(
                    bbox, expand_radio=1, height=frame.shape[0], width=frame.shape[1]
                )

            driven_pose_image = Image.fromarray(frame)
            driven_pose_image = crop_resize_img(driven_pose_image, bbox_s, image_size)
            driven_pose_images_tensor = vasa_transform(driven_pose_image)  # 3, 256, 256
            driven_pose_images_list.append(driven_pose_images_tensor)
            driven_image_tensor = to_tensor(driven_pose_image)
            driven_pose_tensor_list.append(driven_image_tensor)

    sample = dict(
        img_pose=pose_to_tensor(pose_img),
        exp_mask=pose_to_tensor(exp_mask),
        mouth_mask=pose_to_tensor(mouth_mask),
        ref_img=to_tensor(imSrc),
        clip_images=clip_image,
        vasa_face_image=(
            torch.stack(driven_face_images_list, dim=0) if video_path else None
        ),
        vasa_pose_image=(
            torch.stack(driven_pose_images_list, dim=0) if video_path else None
        ),
        driven_expression_tensor_list=(
            torch.stack(driven_expression_tensor_list, dim=0) if video_path else None
        ),
        driven_pose_tensor_list=(
            torch.stack(driven_pose_tensor_list, dim=0) if video_path else None
        ),
        audio_feature=audio_input[0],
        audio_len=audio_len,
    )

    if with_id_encoder:
        from src.utils.arcface import get_model

        id_encoder = get_model("r50")
        weights = torch.load(
            "enhance_model/arc2face/arcface_torch_models/backbone.pth",
            map_location="cpu",
        )
        id_encoder.load_state_dict(weights, strict=True)
        id_encoder.eval().to(device="cuda")

        image_transform = transforms.Compose(
            [
                transforms.Resize(
                    (112, 112), interpolation=transforms.InterpolationMode.BILINEAR
                ),
                transforms.ToTensor(),
            ]
        )
        head_img = image_transform(head_img).unsqueeze(0).float().to(device="cuda")
        head_img = (head_img * 2.0) - 1.0
        head_img = id_encoder(head_img)

        sample = dict(
            img_pose=pose_to_tensor(pose_img),
            exp_mask=pose_to_tensor(exp_mask),
            mouth_mask=pose_to_tensor(mouth_mask),
            ref_img=to_tensor(imSrc),
            clip_images=head_img,
            vasa_face_image=(
                torch.stack(driven_face_images_list, dim=0) if video_path else None
            ),
            vasa_pose_image=(
                torch.stack(driven_pose_images_list, dim=0) if video_path else None
            ),
            driven_expression_tensor_list=(
                torch.stack(driven_expression_tensor_list, dim=0)
                if video_path
                else None
            ),
            driven_pose_tensor_list=(
                torch.stack(driven_pose_tensor_list, dim=0) if video_path else None
            ),
            audio_feature=audio_input[0],
            audio_len=audio_len,
        )
    return sample
