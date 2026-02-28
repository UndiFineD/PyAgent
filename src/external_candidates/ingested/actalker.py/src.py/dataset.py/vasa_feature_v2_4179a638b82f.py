# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\dataset\vasa_feature_v2.py
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torch import nn
from torchvision import transforms


class HeadPose_train(nn.Module):
    def __init__(self):
        super(HeadPose_train, self).__init__()
        self.head_pose_net = ResNet18_GN(num_classes=6)

    def forward(self, x):
        # Forward pass through head pose network
        head_pose = self.head_pose_net(x)
        rotation = head_pose[:, :3]
        translation = head_pose[:, 3:]
        rotation = F.sigmoid(rotation) * 360.0 - 180
        translation = F.sigmoid(translation) * 4.0 - 2
        rtn = {"rotation": rotation, "translation": translation}
        return rtn


class ResNet18_GN(nn.Module):
    def __init__(self, num_classes=1000):
        super(ResNet18_GN, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.GroupNorm(32, 64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(BasicBlock, 64, 2, stride=1)
        self.layer2 = self._make_layer(BasicBlock, 128, 2, stride=2)
        self.layer3 = self._make_layer(BasicBlock, 256, 2, stride=2)
        self.layer4 = self._make_layer(BasicBlock, 512, 2, stride=2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * BasicBlock.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.maxpool(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.GroupNorm(32, planes)
        self.conv2 = nn.Conv2d(
            planes,
            planes * self.expansion,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
        )
        self.bn2 = nn.GroupNorm(32, planes * self.expansion)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes * self.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_planes,
                    planes * self.expansion,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.GroupNorm(32, planes * self.expansion),
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


def center_crop(img_driven, face_bbox, aug_pcavs=False):
    h, w = img_driven.shape[:2]
    x0, y0, x1, y1 = face_bbox[:4]
    center = (int((x0 + x1) / 2), int((y0 + y1) / 2))
    crop_size = int(max(x1 - x0, y1 - y0)) // 2
    if aug_pcavs:
        crop_size = int(crop_size * 1.2)
    new_x0, new_y0, new_x1, new_y1 = (
        center[0] - crop_size,
        center[1] - crop_size,
        center[0] + crop_size,
        center[1] + crop_size,
    )
    pad_left, pad_top, pad_right, pad_bottom = 0, 0, 0, 0
    if new_x0 < 0:
        pad_left, new_x0 = -new_x0, 0
    if new_y0 < 0:
        pad_top, new_y0 = -new_y0, 0
    if new_x1 > w:
        pad_right, new_x1 = new_x1 - w, w
    if new_y1 > h:
        pad_bottom, new_y1 = new_y1 - h, h
    img_mtn = img_driven[new_y0:new_y1, new_x0:new_x1]
    img_mtn = cv2.copyMakeBorder(
        img_mtn,
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )
    return img_mtn


class HeadExpression(nn.Module):
    """
    Estimating head expression.
    """

    def __init__(self, out_feat_dim=1024):
        super(HeadExpression, self).__init__()
        self.resnet50 = resnet50_gn(num_classes=out_feat_dim)

    def forward(self, source_image: torch.Tensor) -> torch.Tensor:
        """
        :param x: image tensor of shape [batch, channels, height, width]
        :return:
        """
        x = self.resnet50(source_image)
        return x


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(
        self, inplanes, planes, stride=1, downsample=None, groups=1, base_width=64
    ):
        super(Bottleneck, self).__init__()
        width = int(planes * (base_width / 64.0)) * groups
        self.conv1 = nn.Conv2d(inplanes, width, kernel_size=1, bias=False)
        self.gn1 = nn.GroupNorm(groups, width)
        self.conv2 = nn.Conv2d(
            width,
            width,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False,
            groups=groups,
        )
        self.gn2 = nn.GroupNorm(groups, width)
        self.conv3 = nn.Conv2d(
            width, planes * self.expansion, kernel_size=1, bias=False
        )
        self.gn3 = nn.GroupNorm(groups, planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.gn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.gn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.gn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


def resnet50_gn(**kwargs):
    model = ResNet_GN(Bottleneck, [3, 4, 6, 3], **kwargs)
    return model


class ResNet_GN(nn.Module):
    def __init__(self, block, layers, num_classes=1000, groups=1, base_width=64):
        super(ResNet_GN, self).__init__()
        self.inplanes = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.gn1 = nn.GroupNorm(groups, 64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(
            block, 64, layers[0], groups=groups, base_width=base_width
        )
        self.layer2 = self._make_layer(
            block, 128, layers[1], stride=2, groups=groups, base_width=base_width
        )
        self.layer3 = self._make_layer(
            block, 256, layers[2], stride=2, groups=groups, base_width=base_width
        )
        self.layer4 = self._make_layer(
            block, 512, layers[3], stride=2, groups=groups, base_width=base_width
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(self, block, planes, blocks, stride=1, groups=1, base_width=64):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(
                    self.inplanes,
                    planes * block.expansion,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.GroupNorm(groups, planes * block.expansion),
            )

        layers = []
        layers.append(
            block(self.inplanes, planes, stride, downsample, groups, base_width)
        )
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(
                block(self.inplanes, planes, groups=groups, base_width=base_width)
            )

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.gn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x


def img2tensor(image, transform=None, device="cuda"):
    if transform is None:
        output_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).to(device)
        output_tensor = output_tensor / 255.0
    else:
        image = Image.fromarray(image)
        output_tensor = transform(image).unsqueeze(0).to(device)
    return output_tensor


@torch.no_grad()
def main():
    device = "cuda"
    image_size = 256
    model_path = "MX31c_32k.ckpt"
    image_path = "1_bil.png"
    transform = transforms.Compose(
        [
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0], [1]),
        ]
    )

    # 加载表情模型
    expression_model = HeadExpression(512).to(device)
    # pose_model = HeadPose_train().to(device)
    pose_model = HeadPose_train()
    checkpoint = torch.load(model_path, map_location="cpu")
    generator = checkpoint["generator"]
    expression_data = {}
    for key in generator:
        if "expression_model." in key:
            expression_data[key[len("expression_model.") :]] = generator[key]

    expression_model.load_state_dict(expression_data, strict=True)
    pose_model.load_state_dict(checkpoint["pose_model"])
    expression_model.to(device)
    pose_model.to(device)
    expression_model.eval()
    pose_model.eval()

    # (1, 3, 256, 256)
    target_image = cv2.imread(image_path)
    inp_image = transform(Image.fromarray(target_image)).cuda().unsqueeze(0)

    pose_out = pose_model(inp_image)
    # (bs, 3)
    rot = pose_out["rotation"]
    # (bs, 3)
    trans = pose_out["translation"]
    # (bs, 512)
    expr = expression_model(inp_image)

    import pdb

    pdb.set_trace()


if __name__ == "__main__":
    main()
