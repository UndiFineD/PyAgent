# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\utils\enhance_teeth\enhance_teeth_pnnx.py
import os
import tempfile
import zipfile

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

try:
    import torchvision
except:
    pass


class Model(nn.Module):
    def __init__(self, path):
        super(Model, self).__init__()

        self.encoder_conv_in = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=3,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_0_0_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=32)
        self.encoder_blocks_0_0_act = nn.ReLU()
        self.convbn2d_0 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_0 = nn.ReLU()
        self.encoder_blocks_0_0_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_1_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(2, 2),
        )
        self.encoder_blocks_1_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=32)
        self.encoder_blocks_1_1_act = nn.ReLU()
        self.convbn2d_1 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_1 = nn.ReLU()
        self.encoder_blocks_1_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_1_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(1, 1),
            out_channels=64,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_2_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(2, 2),
        )
        self.encoder_blocks_2_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=64)
        self.encoder_blocks_2_1_act = nn.ReLU()
        self.convbn2d_2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_2 = nn.ReLU()
        self.encoder_blocks_2_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_2_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(1, 1),
            out_channels=128,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_3_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(2, 2),
        )
        self.encoder_blocks_3_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=128)
        self.encoder_blocks_3_1_act = nn.ReLU()
        self.convbn2d_3 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_3 = nn.ReLU()
        self.encoder_blocks_3_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_3_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(1, 1),
            out_channels=256,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_4_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(2, 2),
        )
        self.encoder_blocks_4_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=256)
        self.encoder_blocks_4_1_act = nn.ReLU()
        self.convbn2d_4 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_4 = nn.ReLU()
        self.encoder_blocks_4_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_4_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_5_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(2, 2),
        )
        self.encoder_blocks_5_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_blocks_5_1_act = nn.ReLU()
        self.convbn2d_5 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_5 = nn.ReLU()
        self.encoder_blocks_5_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_5_2_norm = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_blocks_5_2_q = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_5_2_k = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_5_2_v = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_blocks_5_2_proj_out = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_0_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_mid_blocks_0_act = nn.ReLU()
        self.convbn2d_6 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_6 = nn.ReLU()
        self.encoder_mid_blocks_0_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_1_norm = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_mid_blocks_1_q = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_1_k = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_1_v = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_1_proj_out = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_mid_blocks_2_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_mid_blocks_2_act = nn.ReLU()
        self.convbn2d_7 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_7 = nn.ReLU()
        self.encoder_mid_blocks_2_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.encoder_conv_out_0 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.encoder_conv_out_1 = nn.ReLU()
        self.encoder_conv_out_2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_conv_in = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_0_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_mid_blocks_0_act = nn.ReLU()
        self.convbn2d_8 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_8 = nn.ReLU()
        self.decoder_mid_blocks_0_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_1_norm = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_mid_blocks_1_q = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_1_k = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_1_v = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_1_proj_out = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_mid_blocks_2_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_mid_blocks_2_act = nn.ReLU()
        self.convbn2d_9 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_9 = nn.ReLU()
        self.decoder_mid_blocks_2_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_0_0_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_blocks_0_0_act = nn.ReLU()
        self.convbn2d_10 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_10 = nn.ReLU()
        self.decoder_blocks_0_0_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_0_1_norm = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_blocks_0_1_q = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_0_1_k = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_0_1_v = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_0_1_proj_out = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=512,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_1_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_1_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_blocks_1_1_act = nn.ReLU()
        self.convbn2d_11 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_11 = nn.ReLU()
        self.decoder_blocks_1_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_2_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=512,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_2_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=512)
        self.decoder_blocks_2_1_act = nn.ReLU()
        self.convbn2d_12 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_12 = nn.ReLU()
        self.decoder_blocks_2_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_2_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=512,
            kernel_size=(1, 1),
            out_channels=256,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_3_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=256,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_3_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=256)
        self.decoder_blocks_3_1_act = nn.ReLU()
        self.convbn2d_13 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_13 = nn.ReLU()
        self.decoder_blocks_3_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_3_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=256,
            kernel_size=(1, 1),
            out_channels=128,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_4_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=128,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_4_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=128)
        self.decoder_blocks_4_1_act = nn.ReLU()
        self.convbn2d_14 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_14 = nn.ReLU()
        self.decoder_blocks_4_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_4_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=128,
            kernel_size=(1, 1),
            out_channels=64,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_5_0_conv = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=64,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_5_1_norm1 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=64)
        self.decoder_blocks_5_1_act = nn.ReLU()
        self.convbn2d_15 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.pnnx_unique_15 = nn.ReLU()
        self.decoder_blocks_5_1_conv2 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=32,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_blocks_5_1_residual_func = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=64,
            kernel_size=(1, 1),
            out_channels=32,
            padding=(0, 0),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_conv_out4_0 = nn.BatchNorm2d(affine=True, eps=0.000010, num_features=32)
        self.decoder_conv_out4_1 = nn.Conv2d(
            bias=True,
            dilation=(1, 1),
            groups=1,
            in_channels=32,
            kernel_size=(3, 3),
            out_channels=4,
            padding=(1, 1),
            padding_mode="zeros",
            stride=(1, 1),
        )
        self.decoder_conv_out4_2 = nn.Tanh()

        archive = zipfile.ZipFile(f"{path}/enhance_teeth_231122.bin", "r")
        self.encoder_conv_in.bias = self.load_pnnx_bin_as_parameter(archive, "encoder.conv_in.bias", (32), "float32")
        self.encoder_conv_in.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.conv_in.weight", (32, 3, 3, 3), "float32"
        )
        self.encoder_blocks_0_0_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.0.0.norm1.bias", (32), "float32"
        )
        self.encoder_blocks_0_0_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.0.0.norm1.running_mean", (32), "float32"
        )
        self.encoder_blocks_0_0_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.0.0.norm1.running_var", (32), "float32"
        )
        self.encoder_blocks_0_0_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.0.0.norm1.weight", (32), "float32"
        )
        self.convbn2d_0.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_0.bias", (32), "float32")
        self.convbn2d_0.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_0.weight", (32, 32, 3, 3), "float32"
        )
        self.encoder_blocks_0_0_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.0.0.conv2.bias", (32), "float32"
        )
        self.encoder_blocks_0_0_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.0.0.conv2.weight", (32, 32, 3, 3), "float32"
        )
        self.encoder_blocks_1_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.0.conv.bias", (32), "float32"
        )
        self.encoder_blocks_1_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.0.conv.weight", (32, 32, 3, 3), "float32"
        )
        self.encoder_blocks_1_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.1.norm1.bias", (32), "float32"
        )
        self.encoder_blocks_1_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.1.1.norm1.running_mean", (32), "float32"
        )
        self.encoder_blocks_1_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.1.1.norm1.running_var", (32), "float32"
        )
        self.encoder_blocks_1_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.1.norm1.weight", (32), "float32"
        )
        self.convbn2d_1.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_1.bias", (64), "float32")
        self.convbn2d_1.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_1.weight", (64, 32, 3, 3), "float32"
        )
        self.encoder_blocks_1_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.1.conv2.bias", (64), "float32"
        )
        self.encoder_blocks_1_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.1.conv2.weight", (64, 64, 3, 3), "float32"
        )
        self.encoder_blocks_1_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.1.1.residual_func.bias", (64), "float32"
        )
        self.encoder_blocks_1_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "encoder.blocks.1.1.residual_func.weight",
            (64, 32, 1, 1),
            "float32",
        )
        self.encoder_blocks_2_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.0.conv.bias", (64), "float32"
        )
        self.encoder_blocks_2_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.0.conv.weight", (64, 64, 3, 3), "float32"
        )
        self.encoder_blocks_2_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.1.norm1.bias", (64), "float32"
        )
        self.encoder_blocks_2_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.2.1.norm1.running_mean", (64), "float32"
        )
        self.encoder_blocks_2_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.2.1.norm1.running_var", (64), "float32"
        )
        self.encoder_blocks_2_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.1.norm1.weight", (64), "float32"
        )
        self.convbn2d_2.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_2.bias", (128), "float32")
        self.convbn2d_2.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_2.weight", (128, 64, 3, 3), "float32"
        )
        self.encoder_blocks_2_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.1.conv2.bias", (128), "float32"
        )
        self.encoder_blocks_2_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.1.conv2.weight", (128, 128, 3, 3), "float32"
        )
        self.encoder_blocks_2_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.2.1.residual_func.bias", (128), "float32"
        )
        self.encoder_blocks_2_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "encoder.blocks.2.1.residual_func.weight",
            (128, 64, 1, 1),
            "float32",
        )
        self.encoder_blocks_3_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.0.conv.bias", (128), "float32"
        )
        self.encoder_blocks_3_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.0.conv.weight", (128, 128, 3, 3), "float32"
        )
        self.encoder_blocks_3_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.1.norm1.bias", (128), "float32"
        )
        self.encoder_blocks_3_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.3.1.norm1.running_mean", (128), "float32"
        )
        self.encoder_blocks_3_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.3.1.norm1.running_var", (128), "float32"
        )
        self.encoder_blocks_3_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.1.norm1.weight", (128), "float32"
        )
        self.convbn2d_3.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_3.bias", (256), "float32")
        self.convbn2d_3.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_3.weight", (256, 128, 3, 3), "float32"
        )
        self.encoder_blocks_3_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.1.conv2.bias", (256), "float32"
        )
        self.encoder_blocks_3_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.1.conv2.weight", (256, 256, 3, 3), "float32"
        )
        self.encoder_blocks_3_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.3.1.residual_func.bias", (256), "float32"
        )
        self.encoder_blocks_3_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "encoder.blocks.3.1.residual_func.weight",
            (256, 128, 1, 1),
            "float32",
        )
        self.encoder_blocks_4_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.0.conv.bias", (256), "float32"
        )
        self.encoder_blocks_4_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.0.conv.weight", (256, 256, 3, 3), "float32"
        )
        self.encoder_blocks_4_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.1.norm1.bias", (256), "float32"
        )
        self.encoder_blocks_4_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.4.1.norm1.running_mean", (256), "float32"
        )
        self.encoder_blocks_4_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.4.1.norm1.running_var", (256), "float32"
        )
        self.encoder_blocks_4_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.1.norm1.weight", (256), "float32"
        )
        self.convbn2d_4.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_4.bias", (512), "float32")
        self.convbn2d_4.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_4.weight", (512, 256, 3, 3), "float32"
        )
        self.encoder_blocks_4_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.1.conv2.bias", (512), "float32"
        )
        self.encoder_blocks_4_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.1.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_blocks_4_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.4.1.residual_func.bias", (512), "float32"
        )
        self.encoder_blocks_4_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "encoder.blocks.4.1.residual_func.weight",
            (512, 256, 1, 1),
            "float32",
        )
        self.encoder_blocks_5_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.0.conv.bias", (512), "float32"
        )
        self.encoder_blocks_5_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.0.conv.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_blocks_5_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.1.norm1.bias", (512), "float32"
        )
        self.encoder_blocks_5_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.5.1.norm1.running_mean", (512), "float32"
        )
        self.encoder_blocks_5_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.5.1.norm1.running_var", (512), "float32"
        )
        self.encoder_blocks_5_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.1.norm1.weight", (512), "float32"
        )
        self.convbn2d_5.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_5.bias", (512), "float32")
        self.convbn2d_5.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_5.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_blocks_5_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.1.conv2.bias", (512), "float32"
        )
        self.encoder_blocks_5_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.1.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_blocks_5_2_norm.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.norm.bias", (512), "float32"
        )
        self.encoder_blocks_5_2_norm.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.5.2.norm.running_mean", (512), "float32"
        )
        self.encoder_blocks_5_2_norm.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.blocks.5.2.norm.running_var", (512), "float32"
        )
        self.encoder_blocks_5_2_norm.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.norm.weight", (512), "float32"
        )
        self.encoder_blocks_5_2_q.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.q.bias", (512), "float32"
        )
        self.encoder_blocks_5_2_q.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.q.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_blocks_5_2_k.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.k.bias", (512), "float32"
        )
        self.encoder_blocks_5_2_k.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.k.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_blocks_5_2_v.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.v.bias", (512), "float32"
        )
        self.encoder_blocks_5_2_v.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.v.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_blocks_5_2_proj_out.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.proj_out.bias", (512), "float32"
        )
        self.encoder_blocks_5_2_proj_out.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.blocks.5.2.proj_out.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_mid_blocks_0_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.0.norm1.bias", (512), "float32"
        )
        self.encoder_mid_blocks_0_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.0.norm1.running_mean", (512), "float32"
        )
        self.encoder_mid_blocks_0_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.0.norm1.running_var", (512), "float32"
        )
        self.encoder_mid_blocks_0_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.0.norm1.weight", (512), "float32"
        )
        self.convbn2d_6.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_6.bias", (512), "float32")
        self.convbn2d_6.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_6.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_mid_blocks_0_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.0.conv2.bias", (512), "float32"
        )
        self.encoder_mid_blocks_0_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.0.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_mid_blocks_1_norm.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.norm.bias", (512), "float32"
        )
        self.encoder_mid_blocks_1_norm.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.1.norm.running_mean", (512), "float32"
        )
        self.encoder_mid_blocks_1_norm.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.1.norm.running_var", (512), "float32"
        )
        self.encoder_mid_blocks_1_norm.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.norm.weight", (512), "float32"
        )
        self.encoder_mid_blocks_1_q.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.q.bias", (512), "float32"
        )
        self.encoder_mid_blocks_1_q.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.q.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_mid_blocks_1_k.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.k.bias", (512), "float32"
        )
        self.encoder_mid_blocks_1_k.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.k.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_mid_blocks_1_v.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.v.bias", (512), "float32"
        )
        self.encoder_mid_blocks_1_v.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.v.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_mid_blocks_1_proj_out.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.proj_out.bias", (512), "float32"
        )
        self.encoder_mid_blocks_1_proj_out.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.1.proj_out.weight", (512, 512, 1, 1), "float32"
        )
        self.encoder_mid_blocks_2_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.2.norm1.bias", (512), "float32"
        )
        self.encoder_mid_blocks_2_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.2.norm1.running_mean", (512), "float32"
        )
        self.encoder_mid_blocks_2_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.mid_blocks.2.norm1.running_var", (512), "float32"
        )
        self.encoder_mid_blocks_2_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.2.norm1.weight", (512), "float32"
        )
        self.convbn2d_7.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_7.bias", (512), "float32")
        self.convbn2d_7.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_7.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_mid_blocks_2_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.2.conv2.bias", (512), "float32"
        )
        self.encoder_mid_blocks_2_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.mid_blocks.2.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.encoder_conv_out_0.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.conv_out.0.bias", (512), "float32"
        )
        self.encoder_conv_out_0.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "encoder.conv_out.0.running_mean", (512), "float32"
        )
        self.encoder_conv_out_0.running_var = self.load_pnnx_bin_as_tensor(
            archive, "encoder.conv_out.0.running_var", (512), "float32"
        )
        self.encoder_conv_out_0.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.conv_out.0.weight", (512), "float32"
        )
        self.encoder_conv_out_2.bias = self.load_pnnx_bin_as_parameter(
            archive, "encoder.conv_out.2.bias", (512), "float32"
        )
        self.encoder_conv_out_2.weight = self.load_pnnx_bin_as_parameter(
            archive, "encoder.conv_out.2.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_conv_in.bias = self.load_pnnx_bin_as_parameter(archive, "decoder.conv_in.bias", (512), "float32")
        self.decoder_conv_in.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.conv_in.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_mid_blocks_0_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.0.norm1.bias", (512), "float32"
        )
        self.decoder_mid_blocks_0_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.0.norm1.running_mean", (512), "float32"
        )
        self.decoder_mid_blocks_0_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.0.norm1.running_var", (512), "float32"
        )
        self.decoder_mid_blocks_0_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.0.norm1.weight", (512), "float32"
        )
        self.convbn2d_8.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_8.bias", (512), "float32")
        self.convbn2d_8.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_8.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_mid_blocks_0_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.0.conv2.bias", (512), "float32"
        )
        self.decoder_mid_blocks_0_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.0.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_mid_blocks_1_norm.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.norm.bias", (512), "float32"
        )
        self.decoder_mid_blocks_1_norm.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.1.norm.running_mean", (512), "float32"
        )
        self.decoder_mid_blocks_1_norm.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.1.norm.running_var", (512), "float32"
        )
        self.decoder_mid_blocks_1_norm.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.norm.weight", (512), "float32"
        )
        self.decoder_mid_blocks_1_q.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.q.bias", (512), "float32"
        )
        self.decoder_mid_blocks_1_q.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.q.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_mid_blocks_1_k.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.k.bias", (512), "float32"
        )
        self.decoder_mid_blocks_1_k.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.k.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_mid_blocks_1_v.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.v.bias", (512), "float32"
        )
        self.decoder_mid_blocks_1_v.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.v.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_mid_blocks_1_proj_out.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.proj_out.bias", (512), "float32"
        )
        self.decoder_mid_blocks_1_proj_out.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.1.proj_out.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_mid_blocks_2_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.2.norm1.bias", (512), "float32"
        )
        self.decoder_mid_blocks_2_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.2.norm1.running_mean", (512), "float32"
        )
        self.decoder_mid_blocks_2_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.mid_blocks.2.norm1.running_var", (512), "float32"
        )
        self.decoder_mid_blocks_2_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.2.norm1.weight", (512), "float32"
        )
        self.convbn2d_9.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_9.bias", (512), "float32")
        self.convbn2d_9.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_9.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_mid_blocks_2_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.2.conv2.bias", (512), "float32"
        )
        self.decoder_mid_blocks_2_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.mid_blocks.2.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_0_0_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.0.norm1.bias", (512), "float32"
        )
        self.decoder_blocks_0_0_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.0.0.norm1.running_mean", (512), "float32"
        )
        self.decoder_blocks_0_0_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.0.0.norm1.running_var", (512), "float32"
        )
        self.decoder_blocks_0_0_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.0.norm1.weight", (512), "float32"
        )
        self.convbn2d_10.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_10.bias", (512), "float32")
        self.convbn2d_10.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_10.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_0_0_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.0.conv2.bias", (512), "float32"
        )
        self.decoder_blocks_0_0_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.0.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_0_1_norm.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.norm.bias", (512), "float32"
        )
        self.decoder_blocks_0_1_norm.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.0.1.norm.running_mean", (512), "float32"
        )
        self.decoder_blocks_0_1_norm.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.0.1.norm.running_var", (512), "float32"
        )
        self.decoder_blocks_0_1_norm.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.norm.weight", (512), "float32"
        )
        self.decoder_blocks_0_1_q.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.q.bias", (512), "float32"
        )
        self.decoder_blocks_0_1_q.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.q.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_blocks_0_1_k.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.k.bias", (512), "float32"
        )
        self.decoder_blocks_0_1_k.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.k.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_blocks_0_1_v.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.v.bias", (512), "float32"
        )
        self.decoder_blocks_0_1_v.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.v.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_blocks_0_1_proj_out.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.proj_out.bias", (512), "float32"
        )
        self.decoder_blocks_0_1_proj_out.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.0.1.proj_out.weight", (512, 512, 1, 1), "float32"
        )
        self.decoder_blocks_1_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.0.conv.bias", (512), "float32"
        )
        self.decoder_blocks_1_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.0.conv.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_1_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.1.norm1.bias", (512), "float32"
        )
        self.decoder_blocks_1_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.1.1.norm1.running_mean", (512), "float32"
        )
        self.decoder_blocks_1_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.1.1.norm1.running_var", (512), "float32"
        )
        self.decoder_blocks_1_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.1.norm1.weight", (512), "float32"
        )
        self.convbn2d_11.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_11.bias", (512), "float32")
        self.convbn2d_11.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_11.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_1_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.1.conv2.bias", (512), "float32"
        )
        self.decoder_blocks_1_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.1.1.conv2.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_2_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.0.conv.bias", (512), "float32"
        )
        self.decoder_blocks_2_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.0.conv.weight", (512, 512, 3, 3), "float32"
        )
        self.decoder_blocks_2_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.1.norm1.bias", (512), "float32"
        )
        self.decoder_blocks_2_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.2.1.norm1.running_mean", (512), "float32"
        )
        self.decoder_blocks_2_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.2.1.norm1.running_var", (512), "float32"
        )
        self.decoder_blocks_2_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.1.norm1.weight", (512), "float32"
        )
        self.convbn2d_12.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_12.bias", (256), "float32")
        self.convbn2d_12.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_12.weight", (256, 512, 3, 3), "float32"
        )
        self.decoder_blocks_2_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.1.conv2.bias", (256), "float32"
        )
        self.decoder_blocks_2_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.1.conv2.weight", (256, 256, 3, 3), "float32"
        )
        self.decoder_blocks_2_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.2.1.residual_func.bias", (256), "float32"
        )
        self.decoder_blocks_2_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "decoder.blocks.2.1.residual_func.weight",
            (256, 512, 1, 1),
            "float32",
        )
        self.decoder_blocks_3_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.0.conv.bias", (256), "float32"
        )
        self.decoder_blocks_3_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.0.conv.weight", (256, 256, 3, 3), "float32"
        )
        self.decoder_blocks_3_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.1.norm1.bias", (256), "float32"
        )
        self.decoder_blocks_3_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.3.1.norm1.running_mean", (256), "float32"
        )
        self.decoder_blocks_3_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.3.1.norm1.running_var", (256), "float32"
        )
        self.decoder_blocks_3_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.1.norm1.weight", (256), "float32"
        )
        self.convbn2d_13.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_13.bias", (128), "float32")
        self.convbn2d_13.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_13.weight", (128, 256, 3, 3), "float32"
        )
        self.decoder_blocks_3_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.1.conv2.bias", (128), "float32"
        )
        self.decoder_blocks_3_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.1.conv2.weight", (128, 128, 3, 3), "float32"
        )
        self.decoder_blocks_3_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.3.1.residual_func.bias", (128), "float32"
        )
        self.decoder_blocks_3_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "decoder.blocks.3.1.residual_func.weight",
            (128, 256, 1, 1),
            "float32",
        )
        self.decoder_blocks_4_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.0.conv.bias", (128), "float32"
        )
        self.decoder_blocks_4_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.0.conv.weight", (128, 128, 3, 3), "float32"
        )
        self.decoder_blocks_4_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.1.norm1.bias", (128), "float32"
        )
        self.decoder_blocks_4_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.4.1.norm1.running_mean", (128), "float32"
        )
        self.decoder_blocks_4_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.4.1.norm1.running_var", (128), "float32"
        )
        self.decoder_blocks_4_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.1.norm1.weight", (128), "float32"
        )
        self.convbn2d_14.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_14.bias", (64), "float32")
        self.convbn2d_14.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_14.weight", (64, 128, 3, 3), "float32"
        )
        self.decoder_blocks_4_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.1.conv2.bias", (64), "float32"
        )
        self.decoder_blocks_4_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.1.conv2.weight", (64, 64, 3, 3), "float32"
        )
        self.decoder_blocks_4_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.4.1.residual_func.bias", (64), "float32"
        )
        self.decoder_blocks_4_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "decoder.blocks.4.1.residual_func.weight",
            (64, 128, 1, 1),
            "float32",
        )
        self.decoder_blocks_5_0_conv.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.0.conv.bias", (64), "float32"
        )
        self.decoder_blocks_5_0_conv.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.0.conv.weight", (64, 64, 3, 3), "float32"
        )
        self.decoder_blocks_5_1_norm1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.1.norm1.bias", (64), "float32"
        )
        self.decoder_blocks_5_1_norm1.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.5.1.norm1.running_mean", (64), "float32"
        )
        self.decoder_blocks_5_1_norm1.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.blocks.5.1.norm1.running_var", (64), "float32"
        )
        self.decoder_blocks_5_1_norm1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.1.norm1.weight", (64), "float32"
        )
        self.convbn2d_15.bias = self.load_pnnx_bin_as_parameter(archive, "convbn2d_15.bias", (32), "float32")
        self.convbn2d_15.weight = self.load_pnnx_bin_as_parameter(
            archive, "convbn2d_15.weight", (32, 64, 3, 3), "float32"
        )
        self.decoder_blocks_5_1_conv2.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.1.conv2.bias", (32), "float32"
        )
        self.decoder_blocks_5_1_conv2.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.1.conv2.weight", (32, 32, 3, 3), "float32"
        )
        self.decoder_blocks_5_1_residual_func.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.blocks.5.1.residual_func.bias", (32), "float32"
        )
        self.decoder_blocks_5_1_residual_func.weight = self.load_pnnx_bin_as_parameter(
            archive,
            "decoder.blocks.5.1.residual_func.weight",
            (32, 64, 1, 1),
            "float32",
        )
        self.decoder_conv_out4_0.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.conv_out4.0.bias", (32), "float32"
        )
        self.decoder_conv_out4_0.running_mean = self.load_pnnx_bin_as_tensor(
            archive, "decoder.conv_out4.0.running_mean", (32), "float32"
        )
        self.decoder_conv_out4_0.running_var = self.load_pnnx_bin_as_tensor(
            archive, "decoder.conv_out4.0.running_var", (32), "float32"
        )
        self.decoder_conv_out4_0.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.conv_out4.0.weight", (32), "float32"
        )
        self.decoder_conv_out4_1.bias = self.load_pnnx_bin_as_parameter(
            archive, "decoder.conv_out4.1.bias", (4), "float32"
        )
        self.decoder_conv_out4_1.weight = self.load_pnnx_bin_as_parameter(
            archive, "decoder.conv_out4.1.weight", (4, 32, 3, 3), "float32"
        )
        archive.close()

    def load_pnnx_bin_as_parameter(self, archive, key, shape, dtype, requires_grad=True):
        return nn.Parameter(self.load_pnnx_bin_as_tensor(archive, key, shape, dtype), requires_grad)

    def load_pnnx_bin_as_tensor(self, archive, key, shape, dtype):
        fd, tmppath = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as tmpf, archive.open(key) as keyfile:
            tmpf.write(keyfile.read())
        m = np.memmap(tmppath, dtype=dtype, mode="r", shape=shape).copy()
        os.remove(tmppath)
        return torch.from_numpy(m)

    def forward(self, v_0):
        v_1 = F.upsample(input=v_0, align_corners=False, mode="bicubic", size=(512, 512))
        v_2 = self.encoder_conv_in(v_1)
        v_3 = self.encoder_blocks_0_0_norm1(v_2)
        v_4 = self.encoder_blocks_0_0_act(v_3)
        v_5 = self.convbn2d_0(v_4)
        v_6 = self.pnnx_unique_0(v_5)
        v_7 = self.encoder_blocks_0_0_conv2(v_6)
        v_8 = v_7 + v_2
        v_9 = F.pad(input=v_8, mode="constant", pad=(0, 1, 0, 1), value=0)
        v_10 = self.encoder_blocks_1_0_conv(v_9)
        v_11 = self.encoder_blocks_1_1_norm1(v_10)
        v_12 = self.encoder_blocks_1_1_act(v_11)
        v_13 = self.convbn2d_1(v_12)
        v_14 = self.pnnx_unique_1(v_13)
        v_15 = self.encoder_blocks_1_1_conv2(v_14)
        v_16 = self.encoder_blocks_1_1_residual_func(v_10)
        v_17 = v_15 + v_16
        v_18 = F.pad(input=v_17, mode="constant", pad=(0, 1, 0, 1), value=0)
        v_19 = self.encoder_blocks_2_0_conv(v_18)
        v_20 = self.encoder_blocks_2_1_norm1(v_19)
        v_21 = self.encoder_blocks_2_1_act(v_20)
        v_22 = self.convbn2d_2(v_21)
        v_23 = self.pnnx_unique_2(v_22)
        v_24 = self.encoder_blocks_2_1_conv2(v_23)
        v_25 = self.encoder_blocks_2_1_residual_func(v_19)
        v_26 = v_24 + v_25
        v_27 = F.pad(input=v_26, mode="constant", pad=(0, 1, 0, 1), value=0)
        v_28 = self.encoder_blocks_3_0_conv(v_27)
        v_29 = self.encoder_blocks_3_1_norm1(v_28)
        v_30 = self.encoder_blocks_3_1_act(v_29)
        v_31 = self.convbn2d_3(v_30)
        v_32 = self.pnnx_unique_3(v_31)
        v_33 = self.encoder_blocks_3_1_conv2(v_32)
        v_34 = self.encoder_blocks_3_1_residual_func(v_28)
        v_35 = v_33 + v_34
        v_36 = F.pad(input=v_35, mode="constant", pad=(0, 1, 0, 1), value=0)
        v_37 = self.encoder_blocks_4_0_conv(v_36)
        v_38 = self.encoder_blocks_4_1_norm1(v_37)
        v_39 = self.encoder_blocks_4_1_act(v_38)
        v_40 = self.convbn2d_4(v_39)
        v_41 = self.pnnx_unique_4(v_40)
        v_42 = self.encoder_blocks_4_1_conv2(v_41)
        v_43 = self.encoder_blocks_4_1_residual_func(v_37)
        v_44 = v_42 + v_43
        v_45 = F.pad(input=v_44, mode="constant", pad=(0, 1, 0, 1), value=0)
        v_46 = self.encoder_blocks_5_0_conv(v_45)
        v_47 = self.encoder_blocks_5_1_norm1(v_46)
        v_48 = self.encoder_blocks_5_1_act(v_47)
        v_49 = self.convbn2d_5(v_48)
        v_50 = self.pnnx_unique_5(v_49)
        v_51 = self.encoder_blocks_5_1_conv2(v_50)
        v_52 = v_51 + v_46
        v_53 = self.encoder_blocks_5_2_norm(v_52)
        v_54 = self.encoder_blocks_5_2_q(v_53)
        v_55 = self.encoder_blocks_5_2_k(v_53)
        v_56 = self.encoder_blocks_5_2_v(v_53)
        v_57 = [
            int(v_54.size(0)),
            int(v_54.size(1)),
            int((v_54.size(2) * v_54.size(3))),
        ]
        v_58 = v_54.reshape(*v_57)
        v_59 = torch.permute(input=v_58, dims=(0, 2, 1))
        v_60 = v_55.reshape(*v_57)
        v_61 = torch.bmm(input=v_59, mat2=v_60)
        v_62 = v_61 * 4.419417e-02
        v_63 = F.softmax(input=v_62, dim=2)
        v_64 = v_56.reshape(*v_57)
        v_65 = torch.permute(input=v_63, dims=(0, 2, 1))
        v_66 = torch.bmm(input=v_64, mat2=v_65)
        v_67 = [
            int(v_54.size(0)),
            int(v_54.size(1)),
            int(v_54.size(2)),
            int(v_54.size(3)),
        ]
        v_68 = v_66.reshape(*v_67)
        v_69 = self.encoder_blocks_5_2_proj_out(v_68)
        v_70 = v_52 + v_69
        v_71 = self.encoder_mid_blocks_0_norm1(v_70)
        v_72 = self.encoder_mid_blocks_0_act(v_71)
        v_73 = self.convbn2d_6(v_72)
        v_74 = self.pnnx_unique_6(v_73)
        v_75 = self.encoder_mid_blocks_0_conv2(v_74)
        v_76 = v_75 + v_70
        v_77 = self.encoder_mid_blocks_1_norm(v_76)
        v_78 = self.encoder_mid_blocks_1_q(v_77)
        v_79 = self.encoder_mid_blocks_1_k(v_77)
        v_80 = self.encoder_mid_blocks_1_v(v_77)
        v_81 = [
            int(v_78.size(0)),
            int(v_78.size(1)),
            int((v_78.size(2) * v_78.size(3))),
        ]
        v_82 = v_78.reshape(*v_81)
        v_83 = torch.permute(input=v_82, dims=(0, 2, 1))
        v_84 = v_79.reshape(*v_81)
        v_85 = torch.bmm(input=v_83, mat2=v_84)
        v_86 = v_85 * 4.419417e-02
        v_87 = F.softmax(input=v_86, dim=2)
        v_88 = v_80.reshape(*v_81)
        v_89 = torch.permute(input=v_87, dims=(0, 2, 1))
        v_90 = torch.bmm(input=v_88, mat2=v_89)
        v_91 = [
            int(v_78.size(0)),
            int(v_78.size(1)),
            int(v_78.size(2)),
            int(v_78.size(3)),
        ]
        v_92 = v_90.reshape(*v_91)
        v_93 = self.encoder_mid_blocks_1_proj_out(v_92)
        v_94 = v_76 + v_93
        v_95 = self.encoder_mid_blocks_2_norm1(v_94)
        v_96 = self.encoder_mid_blocks_2_act(v_95)
        v_97 = self.convbn2d_7(v_96)
        v_98 = self.pnnx_unique_7(v_97)
        v_99 = self.encoder_mid_blocks_2_conv2(v_98)
        v_100 = v_99 + v_94
        v_101 = self.encoder_conv_out_0(v_100)
        v_102 = self.encoder_conv_out_1(v_101)
        v_103 = self.encoder_conv_out_2(v_102)
        v_104 = self.decoder_conv_in(v_103)
        v_105 = self.decoder_mid_blocks_0_norm1(v_104)
        v_106 = self.decoder_mid_blocks_0_act(v_105)
        v_107 = self.convbn2d_8(v_106)
        v_108 = self.pnnx_unique_8(v_107)
        v_109 = self.decoder_mid_blocks_0_conv2(v_108)
        v_110 = v_109 + v_104
        v_111 = self.decoder_mid_blocks_1_norm(v_110)
        v_112 = self.decoder_mid_blocks_1_q(v_111)
        v_113 = self.decoder_mid_blocks_1_k(v_111)
        v_114 = self.decoder_mid_blocks_1_v(v_111)
        v_115 = [
            int(v_112.size(0)),
            int(v_112.size(1)),
            int((v_112.size(2) * v_112.size(3))),
        ]
        v_116 = v_112.reshape(*v_115)
        v_117 = torch.permute(input=v_116, dims=(0, 2, 1))
        v_118 = v_113.reshape(*v_115)
        v_119 = torch.bmm(input=v_117, mat2=v_118)
        v_120 = v_119 * 4.419417e-02
        v_121 = F.softmax(input=v_120, dim=2)
        v_122 = v_114.reshape(*v_115)
        v_123 = torch.permute(input=v_121, dims=(0, 2, 1))
        v_124 = torch.bmm(input=v_122, mat2=v_123)
        v_125 = [
            int(v_112.size(0)),
            int(v_112.size(1)),
            int(v_112.size(2)),
            int(v_112.size(3)),
        ]
        v_126 = v_124.reshape(*v_125)
        v_127 = self.decoder_mid_blocks_1_proj_out(v_126)
        v_128 = v_110 + v_127
        v_129 = self.decoder_mid_blocks_2_norm1(v_128)
        v_130 = self.decoder_mid_blocks_2_act(v_129)
        v_131 = self.convbn2d_9(v_130)
        v_132 = self.pnnx_unique_9(v_131)
        v_133 = self.decoder_mid_blocks_2_conv2(v_132)
        v_134 = v_133 + v_128
        v_135 = self.decoder_blocks_0_0_norm1(v_134)
        v_136 = self.decoder_blocks_0_0_act(v_135)
        v_137 = self.convbn2d_10(v_136)
        v_138 = self.pnnx_unique_10(v_137)
        v_139 = self.decoder_blocks_0_0_conv2(v_138)
        v_140 = v_139 + v_134
        v_141 = self.decoder_blocks_0_1_norm(v_140)
        v_142 = self.decoder_blocks_0_1_q(v_141)
        v_143 = self.decoder_blocks_0_1_k(v_141)
        v_144 = self.decoder_blocks_0_1_v(v_141)
        v_145 = [
            int(v_142.size(0)),
            int(v_142.size(1)),
            int((v_142.size(2) * v_142.size(3))),
        ]
        v_146 = v_142.reshape(*v_145)
        v_147 = torch.permute(input=v_146, dims=(0, 2, 1))
        v_148 = v_143.reshape(*v_145)
        v_149 = torch.bmm(input=v_147, mat2=v_148)
        v_150 = v_149 * 4.419417e-02
        v_151 = F.softmax(input=v_150, dim=2)
        v_152 = v_144.reshape(*v_145)
        v_153 = torch.permute(input=v_151, dims=(0, 2, 1))
        v_154 = torch.bmm(input=v_152, mat2=v_153)
        v_155 = [
            int(v_142.size(0)),
            int(v_142.size(1)),
            int(v_142.size(2)),
            int(v_142.size(3)),
        ]
        v_156 = v_154.reshape(*v_155)
        v_157 = self.decoder_blocks_0_1_proj_out(v_156)
        v_158 = v_140 + v_157
        v_159 = F.upsample_nearest(input=v_158, scale_factor=(2.000000, 2.000000))
        v_160 = self.decoder_blocks_1_0_conv(v_159)
        v_161 = self.decoder_blocks_1_1_norm1(v_160)
        v_162 = self.decoder_blocks_1_1_act(v_161)
        v_163 = self.convbn2d_11(v_162)
        v_164 = self.pnnx_unique_11(v_163)
        v_165 = self.decoder_blocks_1_1_conv2(v_164)
        v_166 = v_165 + v_160
        v_167 = F.upsample_nearest(input=v_166, scale_factor=(2.000000, 2.000000))
        v_168 = self.decoder_blocks_2_0_conv(v_167)
        v_169 = self.decoder_blocks_2_1_norm1(v_168)
        v_170 = self.decoder_blocks_2_1_act(v_169)
        v_171 = self.convbn2d_12(v_170)
        v_172 = self.pnnx_unique_12(v_171)
        v_173 = self.decoder_blocks_2_1_conv2(v_172)
        v_174 = self.decoder_blocks_2_1_residual_func(v_168)
        v_175 = v_173 + v_174
        v_176 = F.upsample_nearest(input=v_175, scale_factor=(2.000000, 2.000000))
        v_177 = self.decoder_blocks_3_0_conv(v_176)
        v_178 = self.decoder_blocks_3_1_norm1(v_177)
        v_179 = self.decoder_blocks_3_1_act(v_178)
        v_180 = self.convbn2d_13(v_179)
        v_181 = self.pnnx_unique_13(v_180)
        v_182 = self.decoder_blocks_3_1_conv2(v_181)
        v_183 = self.decoder_blocks_3_1_residual_func(v_177)
        v_184 = v_182 + v_183
        v_185 = F.upsample_nearest(input=v_184, scale_factor=(2.000000, 2.000000))
        v_186 = self.decoder_blocks_4_0_conv(v_185)
        v_187 = self.decoder_blocks_4_1_norm1(v_186)
        v_188 = self.decoder_blocks_4_1_act(v_187)
        v_189 = self.convbn2d_14(v_188)
        v_190 = self.pnnx_unique_14(v_189)
        v_191 = self.decoder_blocks_4_1_conv2(v_190)
        v_192 = self.decoder_blocks_4_1_residual_func(v_186)
        v_193 = v_191 + v_192
        v_194 = F.upsample_nearest(input=v_193, scale_factor=(2.000000, 2.000000))
        v_195 = self.decoder_blocks_5_0_conv(v_194)
        v_196 = self.decoder_blocks_5_1_norm1(v_195)
        v_197 = self.decoder_blocks_5_1_act(v_196)
        v_198 = self.convbn2d_15(v_197)
        v_199 = self.pnnx_unique_15(v_198)
        v_200 = self.decoder_blocks_5_1_conv2(v_199)
        v_201 = self.decoder_blocks_5_1_residual_func(v_195)
        v_202 = v_200 + v_201
        v_203 = self.decoder_conv_out4_0(v_202)
        v_204 = self.decoder_conv_out4_1(v_203)
        v_205 = self.decoder_conv_out4_2(v_204)
        v_206 = v_205[:, :3]
        v_207 = v_205[:, 3:4]
        v_208 = (v_207 + 1) / 2
        v_209 = (
            v_206,
            v_208,
        )
        return v_209


def export_torchscript():
    net = Model()
    net.eval()

    torch.manual_seed(0)
    v_0 = torch.rand(dtype=null)

    mod = torch.jit.trace(net, v_0)
    mod.save("231122_teeth_pnnx.py.pt")


def export_onnx():
    net = Model()
    net.eval()

    torch.manual_seed(0)
    v_0 = torch.rand(dtype=null)

    torch.onnx._export(
        net,
        v_0,
        "231122_teeth_pnnx.py.onnx",
        export_params=True,
        operator_export_type=torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK,
        opset_version=13,
        input_names=["in0"],
        output_names=["out0"],
    )


def test_inference():
    net = Model()
    net.eval()

    torch.manual_seed(0)
    v_0 = torch.rand((1, 3, 512, 512))

    return net(v_0)


if __name__ == "__main__":
    print(test_inference())
