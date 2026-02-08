# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\arcface.py
import torch
from torch import nn
from torch.utils.checkpoint import checkpoint

__all__ = ["iresnet18", "iresnet34", "iresnet50", "iresnet100", "iresnet200"]
using_ckpt = False


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding"""
    return nn.Conv2d(
        in_planes,
        out_planes,
        kernel_size=3,
        stride=stride,
        padding=dilation,
        groups=groups,
        bias=False,
        dilation=dilation,
    )


def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


class IBasicBlock(nn.Module):
    expansion = 1

    def __init__(
        self,
        inplanes,
        planes,
        stride=1,
        downsample=None,
        groups=1,
        base_width=64,
        dilation=1,
    ):
        super(IBasicBlock, self).__init__()
        if groups != 1 or base_width != 64:
            raise ValueError("BasicBlock only supports groups=1 and base_width=64")
        if dilation > 1:
            raise NotImplementedError("Dilation > 1 not supported in BasicBlock")
        self.bn1 = nn.BatchNorm2d(
            inplanes,
            eps=1e-05,
        )
        self.conv1 = conv3x3(inplanes, planes)
        self.bn2 = nn.BatchNorm2d(
            planes,
            eps=1e-05,
        )
        self.prelu = nn.PReLU(planes)
        self.conv2 = conv3x3(planes, planes, stride)
        self.bn3 = nn.BatchNorm2d(
            planes,
            eps=1e-05,
        )
        self.downsample = downsample
        self.stride = stride

    def forward_impl(self, x):
        identity = x
        out = self.bn1(x)
        out = self.conv1(out)
        out = self.bn2(out)
        out = self.prelu(out)
        out = self.conv2(out)
        out = self.bn3(out)
        if self.downsample is not None:
            identity = self.downsample(x)
        out += identity
        return out

    def forward(self, x):
        if self.training and using_ckpt:
            return checkpoint(self.forward_impl, x)
        else:
            return self.forward_impl(x)


class IResNet(nn.Module):
    fc_scale = 7 * 7

    def __init__(
        self,
        block,
        layers,
        dropout=0,
        num_features=512,
        zero_init_residual=False,
        groups=1,
        width_per_group=64,
        replace_stride_with_dilation=None,
        fp16=False,
    ):
        super(IResNet, self).__init__()
        self.extra_gflops = 0.0
        self.fp16 = fp16
        self.inplanes = 64
        self.dilation = 1
        if replace_stride_with_dilation is None:
            replace_stride_with_dilation = [False, False, False]
        if len(replace_stride_with_dilation) != 3:
            raise ValueError(
                "replace_stride_with_dilation should be None or a 3-element tuple, got {}".format(
                    replace_stride_with_dilation
                )
            )
        self.groups = groups
        self.base_width = width_per_group
        self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(self.inplanes, eps=1e-05)
        self.prelu = nn.PReLU(self.inplanes)
        self.layer1 = self._make_layer(block, 64, layers[0], stride=2)
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2, dilate=replace_stride_with_dilation[0])
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2, dilate=replace_stride_with_dilation[1])
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2, dilate=replace_stride_with_dilation[2])
        self.bn2 = nn.BatchNorm2d(
            512 * block.expansion,
            eps=1e-05,
        )
        self.dropout = nn.Dropout(p=dropout, inplace=True)
        self.fc = nn.Linear(512 * block.expansion * self.fc_scale, num_features)
        self.features = nn.BatchNorm1d(num_features, eps=1e-05)
        nn.init.constant_(self.features.weight, 1.0)
        self.features.weight.requires_grad = False

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, 0, 0.1)
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, IBasicBlock):
                    nn.init.constant_(m.bn2.weight, 0)

    def _make_layer(self, block, planes, blocks, stride=1, dilate=False):
        downsample = None
        previous_dilation = self.dilation
        if dilate:
            self.dilation *= stride
            stride = 1
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                conv1x1(self.inplanes, planes * block.expansion, stride),
                nn.BatchNorm2d(
                    planes * block.expansion,
                    eps=1e-05,
                ),
            )
        layers = []
        layers.append(
            block(
                self.inplanes,
                planes,
                stride,
                downsample,
                self.groups,
                self.base_width,
                previous_dilation,
            )
        )
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(
                block(
                    self.inplanes,
                    planes,
                    groups=self.groups,
                    base_width=self.base_width,
                    dilation=self.dilation,
                )
            )

        return nn.Sequential(*layers)

    def forward(self, x):
        with torch.cuda.amp.autocast(self.fp16):
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.prelu(x)
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            x = self.layer4(x)
            x = self.bn2(x)
            x = torch.flatten(x, 1)
            x = self.dropout(x)
        x = self.fc(x.float() if self.fp16 else x)
        x = self.features(x)
        return x


def _iresnet(arch, block, layers, pretrained, progress, **kwargs):
    model = IResNet(block, layers, **kwargs)
    if pretrained:
        raise ValueError()
    return model


def iresnet18(pretrained=False, progress=True, **kwargs):
    return _iresnet("iresnet18", IBasicBlock, [2, 2, 2, 2], pretrained, progress, **kwargs)


def iresnet34(pretrained=False, progress=True, **kwargs):
    return _iresnet("iresnet34", IBasicBlock, [3, 4, 6, 3], pretrained, progress, **kwargs)


def iresnet50(pretrained=False, progress=True, **kwargs):
    return _iresnet("iresnet50", IBasicBlock, [3, 4, 14, 3], pretrained, progress, **kwargs)


def iresnet100(pretrained=False, progress=True, **kwargs):
    return _iresnet("iresnet100", IBasicBlock, [3, 13, 30, 3], pretrained, progress, **kwargs)


def iresnet200(pretrained=False, progress=True, **kwargs):
    return _iresnet("iresnet200", IBasicBlock, [6, 26, 60, 6], pretrained, progress, **kwargs)


def get_model(name, **kwargs):
    # resnet
    if name == "r18":
        return iresnet18(False, **kwargs)
    elif name == "r34":
        return iresnet34(False, **kwargs)
    elif name == "r50":
        return iresnet50(False, **kwargs)
    elif name == "r100":
        return iresnet100(False, **kwargs)
    elif name == "r200":
        return iresnet200(False, **kwargs)
    elif name == "r2060":
        from .iresnet2060 import iresnet2060

        return iresnet2060(False, **kwargs)

    elif name == "mbf":
        fp16 = kwargs.get("fp16", False)
        num_features = kwargs.get("num_features", 512)
        return get_mbf(fp16=fp16, num_features=num_features)

    elif name == "mbf_large":
        from .mobilefacenet import get_mbf_large

        fp16 = kwargs.get("fp16", False)
        num_features = kwargs.get("num_features", 512)
        return get_mbf_large(fp16=fp16, num_features=num_features)

    elif name == "vit_t":
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=256,
            depth=12,
            num_heads=8,
            drop_path_rate=0.1,
            norm_layer="ln",
            mask_ratio=0.1,
        )

    elif name == "vit_t_dp005_mask0":  # For WebFace42M
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=256,
            depth=12,
            num_heads=8,
            drop_path_rate=0.05,
            norm_layer="ln",
            mask_ratio=0.0,
        )

    elif name == "vit_s":
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=512,
            depth=12,
            num_heads=8,
            drop_path_rate=0.1,
            norm_layer="ln",
            mask_ratio=0.1,
        )

    elif name == "vit_s_dp005_mask_0":  # For WebFace42M
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=512,
            depth=12,
            num_heads=8,
            drop_path_rate=0.05,
            norm_layer="ln",
            mask_ratio=0.0,
        )

    elif name == "vit_b":
        # this is a feature
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=512,
            depth=24,
            num_heads=8,
            drop_path_rate=0.1,
            norm_layer="ln",
            mask_ratio=0.1,
            using_checkpoint=True,
        )

    elif name == "vit_b_dp005_mask_005":  # For WebFace42M
        # this is a feature
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=512,
            depth=24,
            num_heads=8,
            drop_path_rate=0.05,
            norm_layer="ln",
            mask_ratio=0.05,
            using_checkpoint=True,
        )

    elif name == "vit_l_dp005_mask_005":  # For WebFace42M
        # this is a feature
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=768,
            depth=24,
            num_heads=8,
            drop_path_rate=0.05,
            norm_layer="ln",
            mask_ratio=0.05,
            using_checkpoint=True,
        )

    elif name == "vit_h":  # For WebFace42M
        num_features = kwargs.get("num_features", 512)
        from .vit import VisionTransformer

        return VisionTransformer(
            img_size=112,
            patch_size=9,
            num_classes=num_features,
            embed_dim=1024,
            depth=48,
            num_heads=8,
            drop_path_rate=0.1,
            norm_layer="ln",
            mask_ratio=0,
            using_checkpoint=True,
        )

    else:
        raise ValueError()


def run_one_image(bbox_list, face_rec, image_transform, image):
    x_min, y_min, x_max, y_max = bbox_list
    face_image = image[int(y_min) : int(y_max), int(x_min) : int(x_max)]
    # thred = 0
    # face_image = image[int(y_min-thred):int(y_max+thred), int(x_min-thred):int(x_max+thred)]
    face_image = Image.fromarray(face_image)

    face_image = image_transform(face_image).unsqueeze(0).float().cuda()
    face_image = (face_image * 2.0) - 1.0
    feat = face_rec(face_image)
    return feat


if __name__ == "__main__":
    import json
    import os

    import imageio
    import numpy as np
    from decord import VideoReader, cpu
    from PIL import Image
    from torchvision import transforms
    from tqdm import tqdm

    model = get_model("r50").to(torch.device("cuda"))
    model.eval()
    weights = torch.load("enhance_model/arc2face/arcface_torch_models/backbone.pth", map_location="cpu")
    model.load_state_dict(weights, strict=True)
    print("done")

    meta_json_1 = "DYBZ/meta_v2/83783db2a23b1e76c81e58e9d01a0324_126_132.json"
    meta_json_2 = "DYBZ/meta_v2/b9954a63552f34936f7a0ea4b50a72b1_168_172.json"
    data_dir = "/apdcephfs_jn/share_302243908/0_public_datasets/talkinghead/all"
    with open(os.path.join(data_dir, meta_json_1), "r") as f:
        meta_data_1 = json.load(f)

    with open(os.path.join(data_dir, meta_json_2), "r") as f:
        meta_data_2 = json.load(f)

    # Resize
    image_transform = transforms.Compose(
        [
            transforms.Resize((112, 112), interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.ToTensor(),
        ]
    )

    same_video = VideoReader(os.path.join(data_dir, meta_data_1["mp4_path"]), ctx=cpu(0))
    diff_video = VideoReader(os.path.join(data_dir, meta_data_2["mp4_path"]), ctx=cpu(0))

    same_video_bbox = meta_data_1["face_list"]
    print(same_video_bbox[0])
    diff_video_bbox = meta_data_2["face_list"]

    same_feats = []
    for idx in tqdm(range(len(same_video))):
        image = same_video[idx].asnumpy()
        feat = run_one_image(
            bbox_list=same_video_bbox[idx],
            face_rec=model,
            image_transform=image_transform,
            image=image,
        )
        same_feats.append(feat)

    same_feats = torch.cat(same_feats, dim=0)

    diff_feats = []
    for idx in tqdm(range(len(diff_video))):
        image = diff_video[idx].asnumpy()
        feat = run_one_image(
            bbox_list=diff_video_bbox[idx],
            face_rec=model,
            image_transform=image_transform,
            image=image,
        )
        diff_feats.append(feat)
    diff_feats = torch.cat(diff_feats, dim=0)
    print(same_feats.shape)
    ref_feat = same_feats[:1]
    same_cos = torch.nn.functional.cosine_similarity(ref_feat.cpu(), same_feats.cpu())
    diff_cos = torch.nn.functional.cosine_similarity(ref_feat.cpu(), diff_feats.cpu())
    print(same_cos)
    print("-" * 50)
    print(diff_cos)
