# Extracted from: C:\DEV\PyAgent\.external\ACTalker\src\models\base\mamba_layer.py
import torch
import torch.nn as nn

try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url

import math
import pdb
from functools import partial
from typing import Callable, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as checkpoint
from diffusers.image_processor import IPAdapterMaskProcessor
from einops import rearrange, repeat
from timm.models.layers import DropPath, to_2tuple, trunc_normal_
from timm.models.resnet import Bottleneck

try:
    from mamba_ssm.ops.selective_scan_interface import (
        selective_scan_fn,
        selective_scan_ref,
    )

    MAMBA_AVAILABLE = True
    print("✓ Mamba SSM loaded successfully")
except ImportError as e:
    print(f"⚠️ Mamba SSM not available: {e}")
    MAMBA_AVAILABLE = False

    # Provide fallback implementations
    def selective_scan_fn(*args, **kwargs):
        raise NotImplementedError(
            "Mamba SSM not available - falling back to standard attention"
        )

    def selective_scan_ref(*args, **kwargs):
        raise NotImplementedError(
            "Mamba SSM not available - falling back to standard attention"
        )


import numpy as np

try:
    from hilbert.hilbert import decode, encode

    print("✓ Hilbert curve functions loaded")
except ImportError as e:
    print(f"⚠️ Hilbert curve not available: {e}")

    def encode(x, y, order=8):
        return x * (2**order) + y

    def decode(d, order=8):
        return [d // (2**order), d % (2**order)]


from pyzorder import ZOrderIndexer


# ========== Decoder ==========
def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
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


def conv1x1(in_planes, out_planes, stride=1) -> nn.Conv2d:
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


def deconv2x2(in_planes, out_planes, stride=1, groups=1, dilation=1):
    return nn.ConvTranspose2d(
        in_planes,
        out_planes,
        kernel_size=2,
        stride=stride,
        groups=groups,
        bias=False,
        dilation=dilation,
    )


class PatchExpand2D(nn.Module):
    def __init__(self, dim, dim_scale=2, norm_layer=nn.LayerNorm):
        super().__init__()
        self.dim = dim * 2
        self.dim_scale = dim_scale
        self.expand = nn.Linear(self.dim, dim_scale * self.dim, bias=False)
        self.norm = norm_layer(self.dim // dim_scale)

    def forward(self, x):
        B, H, W, C = x.shape
        x = self.expand(x)
        x = rearrange(
            x,
            "b h w (p1 p2 c)-> b (h p1) (w p2) c",
            p1=self.dim_scale,
            p2=self.dim_scale,
            c=C // self.dim_scale,
        )
        x = self.norm(x)
        return x


class HSCANS(nn.Module):
    def __init__(
        self,
        size=16,
        dim=2,
        cond_size=0,
        scan_type="scan",
    ):
        super().__init__()
        size = int(size)
        max_num = size**dim + cond_size
        indexes = np.arange(max_num)
        if "sweep" == scan_type:  # ['sweep', 'scan', 'zorder', 'zigzag', 'hilbert']
            locs_flat = indexes
        elif "scan" == scan_type:
            indexes = indexes.reshape(size, size)
            for i in np.arange(1, size, step=2):
                indexes[i, :] = indexes[i, :][::-1]
            locs_flat = indexes.reshape(-1)
        elif "zorder" == scan_type:
            zi = ZOrderIndexer((0, size - 1), (0, size - 1))
            locs_flat = []
            for z in indexes:
                r, c = zi.rc(int(z))
                locs_flat.append(c * size + r)
            locs_flat = np.array(locs_flat)
        elif "zigzag" == scan_type:
            indexes = indexes.reshape(size, size)
            locs_flat = []
            for i in range(2 * size - 1):
                if i % 2 == 0:
                    start_col = max(0, i - size + 1)
                    end_col = min(i, size - 1)
                    for j in range(start_col, end_col + 1):
                        locs_flat.append(indexes[i - j, j])
                else:
                    start_row = max(0, i - size + 1)
                    end_row = min(i, size - 1)
                    for j in range(start_row, end_row + 1):
                        locs_flat.append(indexes[j, i - j])
            locs_flat = np.array(locs_flat)
        elif "hilbert" == scan_type:
            bit = int(math.log2(size))
            locs = decode(indexes, dim, bit)
            locs_flat = self.flat_locs_hilbert(locs, dim, bit)
        else:
            raise Exception("invalid encoder mode")
        locs_flat_inv = np.argsort(locs_flat)
        index_flat = (
            torch.LongTensor(locs_flat.astype(np.int64)).unsqueeze(0).unsqueeze(1)
        )
        index_flat_inv = (
            torch.LongTensor(locs_flat_inv.astype(np.int64)).unsqueeze(0).unsqueeze(1)
        )
        self.index_flat = nn.Parameter(index_flat, requires_grad=False)
        self.index_flat_inv = nn.Parameter(index_flat_inv, requires_grad=False)

    def flat_locs_hilbert(self, locs, num_dim, num_bit):
        ret = []
        l = 2**num_bit
        for i in range(len(locs)):
            loc = locs[i]
            loc_flat = 0
            for j in range(num_dim):
                loc_flat += loc[j] * (l**j)
            ret.append(loc_flat)
        return np.array(ret).astype(np.uint64)

    def __call__(self, img):
        img_encode = self.encode(img)
        return img_encode

    def encode(self, img):
        img_encode = torch.zeros(
            img.shape, dtype=img.dtype, device=img.device
        ).scatter_(2, self.index_flat_inv.expand(img.shape), img)
        return img_encode

    def decode(self, img):
        img_decode = torch.zeros(
            img.shape, dtype=img.dtype, device=img.device
        ).scatter_(2, self.index_flat.expand(img.shape), img)
        return img_decode


class HSCANS_dynamic(nn.Module):
    def __init__(
        self,
        size=16,
        scan_type="scan",
    ):
        super().__init__()
        size = int(size)
        max_num = size
        indexes = np.arange(max_num)
        if "sweep" == scan_type:  # ['sweep', 'scan', 'zorder', 'zigzag', 'hilbert']
            locs_flat = indexes
        elif "scan" == scan_type:
            indexes = indexes.reshape(size, size)
            for i in np.arange(1, size, step=2):
                indexes[i, :] = indexes[i, :][::-1]
            locs_flat = indexes.reshape(-1)
        else:
            raise Exception("invalid encoder mode")
        locs_flat_inv = np.argsort(locs_flat)
        index_flat = (
            torch.LongTensor(locs_flat.astype(np.int64)).unsqueeze(0).unsqueeze(1)
        )
        index_flat_inv = (
            torch.LongTensor(locs_flat_inv.astype(np.int64)).unsqueeze(0).unsqueeze(1)
        )
        self.index_flat = nn.Parameter(index_flat, requires_grad=False)
        self.index_flat_inv = nn.Parameter(index_flat_inv, requires_grad=False)

    def flat_locs_hilbert(self, locs, num_dim, num_bit):
        ret = []
        l = 2**num_bit
        for i in range(len(locs)):
            loc = locs[i]
            loc_flat = 0
            for j in range(num_dim):
                loc_flat += loc[j] * (l**j)
            ret.append(loc_flat)
        return np.array(ret).astype(np.uint64)

    def __call__(self, img):
        img_encode = self.encode(img)
        return img_encode

    def encode(self, img):
        img_encode = torch.zeros(
            img.shape, dtype=img.dtype, device=img.device
        ).scatter_(2, self.index_flat_inv.expand(img.shape), img)
        return img_encode

    def decode(self, img):
        img_decode = torch.zeros(
            img.shape, dtype=img.dtype, device=img.device
        ).scatter_(2, self.index_flat.expand(img.shape), img)
        return img_decode


class SS2D(nn.Module):
    def __init__(
        self,
        d_model,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank

        self.in_proj = nn.Linear(
            self.d_model, self.d_inner * 2, bias=bias, **factory_kwargs
        )
        self.conv2d = nn.Conv2d(
            in_channels=self.d_inner,
            out_channels=self.d_inner,
            groups=self.d_inner,
            bias=conv_bias,
            kernel_size=d_conv,
            padding=(d_conv - 1) // 2,
            **factory_kwargs,
        )
        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scans = HSCANS(size=size, scan_type=scan_type)

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, H, W = x.shape
        L = H * W
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(self.scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                self.scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                self.scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                self.scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.float().view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().float().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.float().view(-1)  # (k * d)
        As = -torch.exp(self.A_logs.float()).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.float().view(-1)  # (k * d)

        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(self.scans.decode(out_y[:, 0]))
            ys.append(self.scans.decode(inv_y[:, 0]))
        if K >= 4:
            ys.append(
                torch.transpose(
                    self.scans.decode(out_y[:, 1]).view(B, -1, W, H), dim0=2, dim1=3
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.transpose(
                    self.scans.decode(inv_y[:, 1]).view(B, -1, W, H), dim0=2, dim1=3
                )
                .contiguous()
                .view(B, -1, L)
            )
        if K >= 8:
            ys.append(
                torch.rot90(
                    self.scans.decode(out_y[:, 2]).view(B, -1, W, H), k=3, dims=(2, 3)
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    self.scans.decode(inv_y[:, 2]).view(B, -1, W, H), k=3, dims=(2, 3)
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    torch.transpose(
                        self.scans.decode(out_y[:, 3]).view(B, -1, W, H), dim0=2, dim1=3
                    ),
                    k=3,
                    dims=(2, 3),
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    torch.transpose(
                        self.scans.decode(inv_y[:, 3]).view(B, -1, W, H), dim0=2, dim1=3
                    ),
                    k=3,
                    dims=(2, 3),
                )
                .contiguous()
                .view(B, -1, L)
            )
        y = sum(ys)
        return y

    def forward_core_seq(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(self.scans.encode(x))
        if K >= 4:
            xs.append(
                self.scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                self.scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                self.scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.float().view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().float().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.float().view(-1)  # (k * d)
        As = -torch.exp(self.A_logs.float()).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.float().view(-1)  # (k * d)

        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(self.scans.decode(out_y[:, 0]))
            ys.append(self.scans.decode(inv_y[:, 0]))
        if K >= 4:
            ys.append(
                torch.transpose(
                    self.scans.decode(out_y[:, 1]).view(B, -1, W, H), dim0=2, dim1=3
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.transpose(
                    self.scans.decode(inv_y[:, 1]).view(B, -1, W, H), dim0=2, dim1=3
                )
                .contiguous()
                .view(B, -1, L)
            )
        if K >= 8:
            ys.append(
                torch.rot90(
                    self.scans.decode(out_y[:, 2]).view(B, -1, W, H), k=3, dims=(2, 3)
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    self.scans.decode(inv_y[:, 2]).view(B, -1, W, H), k=3, dims=(2, 3)
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    torch.transpose(
                        self.scans.decode(out_y[:, 3]).view(B, -1, W, H), dim0=2, dim1=3
                    ),
                    k=3,
                    dims=(2, 3),
                )
                .contiguous()
                .view(B, -1, L)
            )
            ys.append(
                torch.rot90(
                    torch.transpose(
                        self.scans.decode(inv_y[:, 3]).view(B, -1, W, H), dim0=2, dim1=3
                    ),
                    k=3,
                    dims=(2, 3),
                )
                .contiguous()
                .view(B, -1, L)
            )
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, **kwargs):
        B, H, W, C = x.shape
        xz = self.in_proj(x)
        x, z = xz.chunk(2, dim=-1)  # (b, h, w, d)
        x = x.permute(0, 3, 1, 2).contiguous()
        x = self.act(self.conv2d(x))  # (b, d, h, w)
        y = self.forward_core(x)
        y = torch.transpose(y, dim0=1, dim1=2).contiguous().view(B, H, W, -1)
        y = self.out_norm(y)
        y = y * F.silu(z)
        out = self.out_proj(y)
        if self.dropout is not None:
            out = self.dropout(out)
        return out


class SS2D_cond(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.fuse_proj = nn.Linear(self.d_inner*2, self.d_inner, bias=bias, **factory_kwargs)
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )
        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.float().view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().float().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.float().view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.float().view(-1)  # (k * d)
        As = -torch.exp(self.A_logs.float()).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.float().view(-1)  # (k * d)

        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond).squeeze(1)  # (b, c, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        # x = self.act(self.conv2d(x))  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input)
        y = y.to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        out = x + y
        return out


class SS2D_cond_v2(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.fuse_proj = nn.Linear(self.d_inner*2, self.d_inner, bias=bias, **factory_kwargs)
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )
        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond).repeat(B, 1, 1)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        # x = self.act(self.conv2d(x))  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input).to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


# cond input size is [bs,n,c]
class SS2D_cond_v3(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.fuse_proj = nn.Linear(self.d_inner*2, self.d_inner, bias=bias, **factory_kwargs)
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )
        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        # x = self.act(self.conv2d(x))  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input).to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


# cond input size is [bs,n,c]
# add sigmoid
class SS2D_cond_v4(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input).to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


# all params are in forward
class SS2D_cond_v7(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, latent_L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        x = input.permute(0, 2, 1).contiguous()

        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys).to(xz.dtype)
        y = y[:, :, :latent_L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


# cond input size is [bs,n,c]
# add sigmoid
class SS2D_cond_v4_wo_ssd(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None

        self.mid_fc = nn.Sequential(
            nn.Linear(self.d_inner, self.d_inner),
            nn.SiLU(),
            nn.Linear(self.d_inner, self.d_inner),
            nn.SiLU(),
            nn.Linear(self.d_inner, self.d_inner),
            nn.SiLU(),
            nn.Linear(self.d_inner, self.d_inner),
            nn.SiLU(),
        )

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        y = self.mid_fc(input)
        y = y[:, :L, :]
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_Unit(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, input):
        y = self.forward_core(input)
        return y


class SS2D_cond_v5(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        n_ssd_unit=2,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.n_ssd_unit = n_ssd_unit
        self.ssd_unit = nn.ModuleList(
            [
                SS2D_Unit(
                    d_model,
                    d_cond,
                    cond_size,
                    d_state,
                    d_conv,
                    expand,
                    dt_rank,
                    dt_min,
                    dt_max,
                    dt_init,
                    dt_scale,
                    dt_init_floor,
                    dropout,
                    conv_bias,
                    bias,
                    device,
                    dtype,
                    size,
                    scan_type,
                    num_direction,
                )
                for _ in range(n_ssd_unit)
            ]
        )
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        input = input.permute(0, 2, 1).contiguous()
        rst = []
        for ssd_unit in self.ssd_unit:
            rst.append(ssd_unit(input).to(xz.dtype))
        y = torch.mean(torch.stack(rst, dim=0), dim=0)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_cond_v6(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        n_ssd_unit=4,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.n_ssd_unit = n_ssd_unit
        self.intra_ssm = SS2D_Unit(
            d_model,
            d_cond,
            0,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )
        self.cond_ssm = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        xz = (
            self.intra_ssm(xz.permute(0, 2, 1).contiguous())
            .permute(0, 2, 1)
            .contiguous()
        )
        cond_proj = self.cond_proj(cond)  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        input = input.permute(0, 2, 1).contiguous()
        y = self.cond_ssm(input)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_cond_v8(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.audio_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.exp_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.audio_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.exp_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.id_proj = nn.Linear(self.d_cond, self.d_inner, bias=bias, **factory_kwargs)

        self.in_proj1 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj2 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.act1 = nn.SiLU()
        self.act2 = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x, id_emb, conds, masks):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        audio_cond = conds[:, :-1]
        exp_cond = conds[:, -1:]
        id_emb = self.act2(self.id_proj(id_emb))
        xz1 = self.in_proj1(x)
        xz2 = self.in_proj2(x)
        xz1 = torch.cat([xz1, id_emb], dim=1)
        xz2 = torch.cat([xz2, id_emb], dim=1)
        audio_cond = self.act1(self.audio_proj(audio_cond))
        audio_input = torch.cat([xz1, audio_cond], dim=1)
        audio_input = audio_input.permute(0, 2, 1)
        audio_output = self.audio_unit(audio_input).to(xz1.dtype)
        audio_rst = audio_output[:, :, :L].permute(0, 2, 1)
        audio_mask = IPAdapterMaskProcessor.downsample(
            masks[0][:, 0, :, :],
            masks[0].shape[0],
            audio_rst.shape[1],
            audio_rst.shape[2],
        )
        audio_rst = audio_rst * audio_mask

        exp_cond = self.act2(self.exp_proj(exp_cond))
        exp_input = torch.cat([xz2, exp_cond], dim=1)
        exp_input = exp_input.permute(0, 2, 1)
        exp_output = self.exp_unit(exp_input).to(xz2.dtype)
        exp_rst = exp_output[:, :, :L].permute(0, 2, 1)
        exp_mask = IPAdapterMaskProcessor.downsample(
            masks[1][:, 0, :, :],
            masks[1].shape[0],
            exp_rst.shape[1],
            exp_rst.shape[2],
        )
        exp_rst = exp_rst * exp_mask
        y = audio_rst + exp_rst
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_cond_v9(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.audio_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.exp_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.fuse_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.audio_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.exp_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.id_proj = nn.Linear(self.d_cond, self.d_inner, bias=bias, **factory_kwargs)

        self.in_proj1 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj2 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.act1 = nn.SiLU()
        self.act2 = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x, id_emb, conds, masks):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        audio_cond = conds[:, :-1]
        exp_cond = conds[:, -1:]
        id_emb = self.act2(self.id_proj(id_emb))
        xz1 = self.in_proj1(x)
        xz2 = self.in_proj2(x)
        xz1 = torch.cat([xz1, id_emb], dim=1)
        xz2 = torch.cat([xz2, id_emb], dim=1)
        audio_cond = self.act1(self.audio_proj(audio_cond))
        audio_input = torch.cat([xz1, audio_cond], dim=1)
        audio_input = audio_input.permute(0, 2, 1)
        audio_output = self.audio_unit(audio_input).to(xz1.dtype)
        audio_rst = audio_output[:, :, :L].permute(0, 2, 1)
        audio_mask = IPAdapterMaskProcessor.downsample(
            masks[0][:, 0, :, :],
            masks[0].shape[0],
            audio_rst.shape[1],
            audio_rst.shape[2],
        )
        audio_rst = audio_rst * audio_mask

        exp_cond = self.act2(self.exp_proj(exp_cond))
        exp_input = torch.cat([xz2, exp_cond], dim=1)
        exp_input = exp_input.permute(0, 2, 1)
        exp_output = self.exp_unit(exp_input).to(xz2.dtype)
        exp_rst = exp_output[:, :, :L].permute(0, 2, 1)
        exp_mask = IPAdapterMaskProcessor.downsample(
            masks[1][:, 0, :, :],
            masks[1].shape[0],
            exp_rst.shape[1],
            exp_rst.shape[2],
        )
        exp_rst = exp_rst * exp_mask
        y = audio_rst + exp_rst

        y = y.permute(0, 2, 1)
        y = self.fuse_unit(y).permute(0, 2, 1)
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


# Mask
class SS2D_cond_v10(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.audio_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.exp_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.audio_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.exp_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.id_proj = nn.Linear(self.d_cond, self.d_inner, bias=bias, **factory_kwargs)

        self.in_proj1 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj2 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.act1 = nn.SiLU()
        self.act2 = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x, id_emb, conds, masks):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        audio_cond = conds[:, :-1]
        exp_cond = conds[:, -1:]
        id_emb = self.act2(self.id_proj(id_emb))
        xz1 = self.in_proj1(x)
        audio_mask = IPAdapterMaskProcessor.downsample(
            masks[0][:, 0, :, :], masks[0].shape[0], xz1.shape[1], 1
        )
        select_tokens = xz1[:, audio_mask.view(-1).int().nonzero().view(-1), :]
        num_tokens = select_tokens.shape[1]
        tokens = torch.cat([select_tokens, id_emb], dim=1)
        audio_cond = self.act1(self.audio_proj(audio_cond))
        audio_input = torch.cat([tokens, audio_cond], dim=1)
        audio_output = self.audio_unit(audio_input.permute(0, 2, 1)).to(xz1.dtype)
        audio_rst = audio_output[:, :, :num_tokens].permute(0, 2, 1)
        xz1[:, audio_mask.view(-1).int().nonzero().view(-1), :] = audio_rst

        xz2 = self.in_proj2(x)
        exp_mask = IPAdapterMaskProcessor.downsample(
            masks[1][:, 0, :, :], masks[1].shape[0], xz2.shape[1], 1
        )
        select_tokens = xz2[:, exp_mask.view(-1).int().nonzero().view(-1), :]
        num_tokens = select_tokens.shape[1]
        tokens = torch.cat([select_tokens, id_emb], dim=1)
        exp_cond = self.act2(self.exp_proj(exp_cond))
        exp_input = torch.cat([tokens, exp_cond], dim=1)
        exp_output = self.exp_unit(exp_input.permute(0, 2, 1)).to(xz2.dtype)
        exp_rst = exp_output[:, :, :num_tokens].permute(0, 2, 1)
        xz2[:, exp_mask.view(-1).int().nonzero().view(-1), :] = exp_rst

        y = xz2 + xz1
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_cond_v10_wo_id(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.audio_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )

        self.exp_unit = SS2D_Unit(
            d_model,
            d_cond,
            cond_size,
            d_state,
            d_conv,
            expand,
            dt_rank,
            dt_min,
            dt_max,
            dt_init,
            dt_scale,
            dt_init_floor,
            dropout,
            conv_bias,
            bias,
            device,
            dtype,
            size,
            scan_type,
            num_direction,
        )
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.audio_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.exp_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )

        self.in_proj1 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj2 = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        self.act1 = nn.SiLU()
        self.act2 = nn.SiLU()
        self.num_direction = num_direction

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    def forward(self, x, id_emb, conds, masks):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        audio_cond = conds[:, :-1]
        exp_cond = conds[:, -1:]
        xz1 = self.in_proj1(x)
        audio_mask = IPAdapterMaskProcessor.downsample(
            masks[0][:, 0, :, :], masks[0].shape[0], xz1.shape[1], 1
        )
        select_tokens = xz1[:, audio_mask.view(-1).int().nonzero().view(-1), :]
        num_tokens = select_tokens.shape[1]
        tokens = select_tokens
        audio_cond = self.act1(self.audio_proj(audio_cond))
        audio_input = torch.cat([tokens, audio_cond], dim=1)
        audio_output = self.audio_unit(audio_input.permute(0, 2, 1)).to(xz1.dtype)
        audio_rst = audio_output[:, :, :num_tokens].permute(0, 2, 1)
        xz1[:, audio_mask.view(-1).int().nonzero().view(-1), :] = audio_rst

        xz2 = self.in_proj2(x)
        exp_mask = IPAdapterMaskProcessor.downsample(
            masks[1][:, 0, :, :], masks[1].shape[0], xz2.shape[1], 1
        )
        select_tokens = xz2[:, exp_mask.view(-1).int().nonzero().view(-1), :]
        num_tokens = select_tokens.shape[1]
        tokens = select_tokens
        exp_cond = self.act2(self.exp_proj(exp_cond))
        exp_input = torch.cat([tokens, exp_cond], dim=1)
        exp_output = self.exp_unit(exp_input.permute(0, 2, 1)).to(xz2.dtype)
        exp_rst = exp_output[:, :, :num_tokens].permute(0, 2, 1)
        xz2[:, exp_mask.view(-1).int().nonzero().view(-1), :] = exp_rst

        y = xz2 + xz1
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_cond_v8_fake(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        self.cond_proj = nn.Linear(
            self.d_cond, self.d_inner, bias=bias, **factory_kwargs
        )
        self.fuse_proj = nn.Linear(
            self.d_inner, self.d_inner, bias=bias, **factory_kwargs
        )
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )

        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x, cond, masks):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        cond_proj = self.cond_proj(torch.cat(cond, dim=1))  # (b, l, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        input = torch.cat([xz, cond_proj], dim=1)
        input = self.act(self.fuse_proj(input))  # (b, l, d)
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input).to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class SS2D_seq(nn.Module):
    def __init__(
        self,
        d_model,
        d_cond,
        cond_size=0,
        d_state=16,
        d_conv=3,
        expand=2,
        dt_rank="auto",
        dt_min=0.001,
        dt_max=0.1,
        dt_init="random",
        dt_scale=1.0,
        dt_init_floor=1e-4,
        dropout=0.0,
        conv_bias=True,
        bias=False,
        device=None,
        dtype=None,
        size=8,
        scan_type="scan",
        num_direction=8,
        **kwargs,
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        self.dt_rank = math.ceil(self.d_model / 16) if dt_rank == "auto" else dt_rank
        self.d_cond = d_cond
        # self.fuse_proj = nn.Linear(self.d_inner*2, self.d_inner, bias=bias, **factory_kwargs)
        self.in_proj = nn.Linear(
            self.d_model, self.d_inner, bias=bias, **factory_kwargs
        )
        # self.conv2d = nn.Conv2d(
        #     in_channels=self.d_inner,
        #     out_channels=self.d_inner,
        #     groups=self.d_inner,
        #     bias=conv_bias,
        #     kernel_size=d_conv,
        #     padding=(d_conv - 1) // 2,
        #     **factory_kwargs,
        # )
        self.act = nn.SiLU()
        self.num_direction = num_direction

        x_proj_weight = [
            nn.Linear(
                self.d_inner,
                (self.dt_rank + self.d_state * 2),
                bias=False,
                **factory_kwargs,
            ).weight
            for _ in range(self.num_direction)
        ]
        self.x_proj_weight = nn.Parameter(torch.stack(x_proj_weight, dim=0))
        dt_projs = [
            self.dt_init(
                self.dt_rank,
                self.d_inner,
                dt_scale,
                dt_init,
                dt_min,
                dt_max,
                dt_init_floor,
                **factory_kwargs,
            )
            for _ in range(self.num_direction)
        ]
        self.dt_projs_weight = nn.Parameter(
            torch.stack([dt_proj.weight for dt_proj in dt_projs], dim=0)
        )
        self.dt_projs_bias = nn.Parameter(
            torch.stack([dt_proj.bias for dt_proj in dt_projs], dim=0)
        )

        self.A_logs = self.A_log_init(
            self.d_state, self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.Ds = self.D_init(
            self.d_inner, copies=self.num_direction, merge=True
        )  # (K=4, D, N)
        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(
            self.d_inner, self.d_model, bias=bias, **factory_kwargs
        )
        self.dropout = nn.Dropout(dropout) if dropout > 0.0 else None
        self.scan_type = scan_type

    @staticmethod
    def dt_init(
        dt_rank,
        d_inner,
        dt_scale=1.0,
        dt_init="random",
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        **factory_kwargs,
    ):
        dt_proj = nn.Linear(dt_rank, d_inner, bias=True, **factory_kwargs)
        # Initialize special dt projection to preserve variance at initialization
        dt_init_std = dt_rank**-0.5 * dt_scale
        if dt_init == "constant":
            nn.init.constant_(dt_proj.weight, dt_init_std)
        elif dt_init == "random":
            nn.init.uniform_(dt_proj.weight, -dt_init_std, dt_init_std)
        else:
            raise NotImplementedError
        # Initialize dt bias so that F.softplus(dt_bias) is between dt_min and dt_max
        dt = torch.exp(
            torch.rand(d_inner, **factory_kwargs)
            * (math.log(dt_max) - math.log(dt_min))
            + math.log(dt_min)
        ).clamp(min=dt_init_floor)
        # Inverse of softplus: https://github.com/pytorch/pytorch/issues/72759
        inv_dt = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            dt_proj.bias.copy_(inv_dt)
        # Our initialization would set all Linear.bias to zero, need to mark this one as _no_reinit
        dt_proj.bias._no_reinit = True
        return dt_proj

    @staticmethod
    def A_log_init(d_state, d_inner, copies=1, device=None, merge=True):
        # S4D real initialization
        A = repeat(
            torch.arange(1, d_state + 1, dtype=torch.float32, device=device),
            "n -> d n",
            d=d_inner,
        ).contiguous()
        A_log = torch.log(A)  # Keep A_log in fp32
        if copies > 1:
            A_log = repeat(A_log, "d n -> r d n", r=copies)
            if merge:
                A_log = A_log.flatten(0, 1)
        A_log = nn.Parameter(A_log)
        # A_log._no_weight_decay = True
        return A_log

    @staticmethod
    def D_init(d_inner, copies=1, device=None, merge=True):
        # D "skip" parameter
        D = torch.ones(d_inner, device=device, dtype=torch.float32)
        if copies > 1:
            D = repeat(D, "n1 -> r n1", r=copies)
            if merge:
                D = D.flatten(0, 1)
        D = nn.Parameter(D)  # Keep in fp32
        # D._no_weight_decay = True
        return D

    def forward_core(self, x: torch.Tensor):
        self.selective_scan = selective_scan_fn
        B, C, L = x.shape
        scans = HSCANS_dynamic(size=L, scan_type=self.scan_type).to(x.device)
        K = self.num_direction
        xs = []
        if K >= 2:
            xs.append(scans.encode(x.view(B, -1, L)))
        if K >= 4:
            xs.append(
                scans.encode(
                    torch.transpose(x, dim0=2, dim1=3).contiguous().view(B, -1, L)
                )
            )
        if K >= 8:
            xs.append(
                scans.encode(
                    torch.rot90(x, k=1, dims=(2, 3)).contiguous().view(B, -1, L)
                )
            )
            xs.append(
                scans.encode(
                    torch.transpose(torch.rot90(x, k=1, dims=(2, 3)), dim0=2, dim1=3)
                    .contiguous()
                    .view(B, -1, L)
                )
            )
        xs = torch.stack(xs, dim=1).view(B, K // 2, -1, L)
        xs = torch.cat([xs, torch.flip(xs, dims=[-1])], dim=1)

        x_dbl = torch.einsum(
            "b k d l, k c d -> b k c l", xs.view(B, K, -1, L), self.x_proj_weight
        )
        dts, Bs, Cs = torch.split(
            x_dbl, [self.dt_rank, self.d_state, self.d_state], dim=2
        )
        dts = torch.einsum(
            "b k r l, k d r -> b k d l", dts.view(B, K, -1, L), self.dt_projs_weight
        )

        xs = xs.view(B, -1, L)  # (b, k * d, l)
        dts = dts.contiguous().view(B, -1, L)  # (b, k * d, l)
        Bs = Bs.view(B, K, -1, L)  # (b, k, d_state, l)
        Cs = Cs.view(B, K, -1, L)  # (b, k, d_state, l)
        Ds = self.Ds.view(-1)  # (k * d)
        As = -torch.exp(self.A_logs).view(-1, self.d_state)  # (k * d, d_state)
        dt_projs_bias = self.dt_projs_bias.view(-1)  # (k * d)
        out_y = self.selective_scan(
            xs,
            dts,
            As,
            Bs,
            Cs,
            Ds,
            z=None,
            delta_bias=dt_projs_bias,
            delta_softplus=True,
            return_last_state=False,
        ).view(B, K, -1, L)
        # assert out_y.dtype == torch.float
        # out_y = xs

        inv_y = torch.flip(out_y[:, K // 2 : K], dims=[-1]).view(B, K // 2, -1, L)
        ys = []
        if K >= 2:
            ys.append(scans.decode(out_y[:, 0]))
            ys.append(scans.decode(inv_y[:, 0]))
        y = sum(ys)
        return y

    def forward(self, x: torch.Tensor, cond: torch.Tensor = None, **kwargs):
        # cond is (b, 1, c, d_cond)
        B, L, C = x.shape
        xz = self.in_proj(x)
        # cond_proj = self.cond_proj(cond).squeeze(1) # (b, c, d_cond)
        # x, z = xz.chunk(2, dim=-1)  # (b, l, d)
        # x = self.act(self.conv2d(x))  # (b, l, d)
        input = xz
        input = input.permute(0, 2, 1).contiguous()
        y = self.forward_core(input).to(xz.dtype)
        y = y[:, :, :L].permute(0, 2, 1).contiguous()
        y = self.out_norm(y)
        y = self.out_proj(y)
        return y


class HSSBlock(nn.Module):
    def __init__(
        self,
        hidden_dim: int = 0,
        drop_path: float = 0,
        norm_layer: Callable[..., torch.nn.Module] = partial(nn.LayerNorm, eps=1e-6),
        attn_drop_rate: float = 0,
        d_state: int = 16,
        size: int = 8,
        scan_type="scan",
        num_direction=4,
        **kwargs,
    ):
        super().__init__()
        self.ln_1 = norm_layer(hidden_dim)
        print(
            "d_model",
            hidden_dim,
            "d_state",
            d_state,
            "size",
            size,
            "scan_type",
            scan_type,
            "num_direction",
            num_direction,
        )
        self.self_attention = SS2D(
            d_model=hidden_dim,
            dropout=attn_drop_rate,
            d_state=d_state,
            size=size,
            scan_type=scan_type,
            num_direction=num_direction,
            **kwargs,
        )
        self.drop_path = DropPath(drop_path)

    def forward(self, input: torch.Tensor):
        x = input + self.drop_path(self.self_attention(self.ln_1(input)))
        return x


class LSSModule(nn.Module):
    def __init__(
        self,
        hidden_dim: int = 0,
        drop_path: float = 0,
        norm_layer: Callable[..., torch.nn.Module] = partial(nn.LayerNorm, eps=1e-6),
        attn_drop_rate: float = 0,
        d_state: int = 16,
        depth: int = 2,
        size: int = 8,
        scan_type: str = "scan",
        num_direction: int = 8,
        **kwargs,
    ):
        super().__init__()
        self.smm_blocks = nn.ModuleList(
            [
                HSSBlock(
                    hidden_dim=hidden_dim,
                    drop_path=drop_path,
                    norm_layer=norm_layer,
                    attn_drop_rate=attn_drop_rate,
                    d_state=d_state,
                    size=size,
                    scan_type=scan_type,
                    num_direction=num_direction,
                    **kwargs,
                )
                for i in range(depth)
            ]
        )
        self.conv1b7 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim, out_channels=hidden_dim, kernel_size=1, stride=1
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.conv1a7 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim, out_channels=hidden_dim, kernel_size=1, stride=1
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.conv1b5 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim, out_channels=hidden_dim, kernel_size=1, stride=1
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.conv1a5 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim, out_channels=hidden_dim, kernel_size=1, stride=1
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.conv55 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim,
                out_channels=hidden_dim,
                kernel_size=5,
                stride=1,
                padding=2,
                bias=False,
                groups=hidden_dim,
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.conv77 = nn.Sequential(
            nn.Conv2d(
                in_channels=hidden_dim,
                out_channels=hidden_dim,
                kernel_size=7,
                stride=1,
                padding=3,
                bias=False,
                groups=hidden_dim,
            ),
            nn.InstanceNorm2d(hidden_dim),
            nn.SiLU(),
        )
        self.finalconv11 = nn.Conv2d(
            in_channels=hidden_dim * 3, out_channels=hidden_dim, kernel_size=1, stride=1
        )
        self.apply(self._init_weights)

    def _init_weights(self, m):
        """
        initialization
        """
        if isinstance(m, nn.Conv2d):
            fan_out = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
            fan_out //= m.groups
            m.weight.data.normal_(0, math.sqrt(2.0 / fan_out))
            if m.bias is not None:
                m.bias.data.zero_()
        # elif isinstance(m, nn.InstanceNorm2d):
        # 	m.weight.data.fill_(1)
        # 	m.bias.data.zero_()

    def forward(self, input: torch.Tensor):
        out_ssm = input
        for blk in self.smm_blocks:
            out_ssm = blk(out_ssm)
        input_conv = input.permute(0, 3, 1, 2).contiguous()
        out_77 = self.conv1a7(self.conv77(self.conv1b7(input_conv)))
        out_55 = self.conv1a5(self.conv55(self.conv1b5(input_conv)))
        output = torch.cat(
            (out_ssm.permute(0, 3, 1, 2).contiguous(), out_55, out_77), dim=1
        )
        output = self.finalconv11(output).permute(0, 2, 3, 1).contiguous()
        return output + input


class LSSLayer_up(nn.Module):
    """A basic Swin Transformer layer for one stage.
    Args:
        dim (int): Number of input channels.
        depth (int): Number of blocks.
        drop (float, optional): Dropout rate. Default: 0.0
        attn_drop (float, optional): Attention dropout rate. Default: 0.0
        drop_path (float | tuple[float], optional): Stochastic depth rate. Default: 0.0
        norm_layer (nn.Module, optional): Normalization layer. Default: nn.LayerNorm
        downsample (nn.Module | None, optional): Downsample layer at the end of the layer. Default: None
        use_checkpoint (bool): Whether to use checkpointing to save memory. Default: False.
    """

    def __init__(
        self,
        dim,
        depth,
        attn_drop=0.0,
        drop_path=0.0,
        norm_layer=nn.LayerNorm,
        upsample=None,
        use_checkpoint=False,
        d_state=16,
        size=8,
        scan_type="scan",
        num_direction=4,
        **kwargs,
    ):
        super().__init__()
        self.dim = dim
        self.use_checkpoint = use_checkpoint

        if depth % 3 == 0:
            self.blocks = nn.ModuleList(
                [
                    LSSModule(
                        hidden_dim=dim,
                        drop_path=(
                            drop_path[i] if isinstance(drop_path, list) else drop_path
                        ),
                        norm_layer=norm_layer,
                        attn_drop_rate=attn_drop,
                        d_state=d_state,
                        size=size,
                        scan_type=scan_type,
                        depth=3,
                        num_direction=num_direction,
                    )
                    for i in range(depth // 3)
                ]
            )
        elif depth % 2 == 0:
            self.blocks = nn.ModuleList(
                [
                    LSSModule(
                        hidden_dim=dim,
                        drop_path=(
                            drop_path[i] if isinstance(drop_path, list) else drop_path
                        ),
                        norm_layer=norm_layer,
                        attn_drop_rate=attn_drop,
                        d_state=d_state,
                        size=size,
                        scan_type=scan_type,
                        depth=2,
                        num_direction=num_direction,
                    )
                    for i in range(depth // 2)
                ]
            )

        if True:  # is this really applied? Yes, but been overriden later in VSSM!

            def _init_weights(module: nn.Module):
                for name, p in module.named_parameters():
                    if name in ["out_proj.weight"]:
                        p = p.clone().detach_()  # fake init, just to keep the seed ....
                        nn.init.kaiming_uniform_(p, a=math.sqrt(5))

            self.apply(_init_weights)

        if upsample is not None:
            self.upsample = upsample(dim=dim, norm_layer=norm_layer)
        else:
            self.upsample = None

    def forward(self, x):
        if self.upsample is not None:
            x = self.upsample(x)
        for blk in self.blocks:
            if self.use_checkpoint:
                x = checkpoint.checkpoint(blk, x)
            else:
                x = blk(x)
        return x


class MambaUPNet(nn.Module):
    def __init__(
        self,
        dims_decoder=[512, 256, 128, 64],
        depths_decoder=[3, 4, 6, 3],
        d_state=16,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        drop_path_rate=0.2,
        norm_layer=nn.LayerNorm,
        scan_type="scan",
        num_direction=4,
    ):
        super().__init__()
        dpr_decoder = [
            x.item() for x in torch.linspace(0, drop_path_rate, sum(depths_decoder))
        ][::-1]
        self.layers_up = nn.ModuleList()
        for i_layer in range(len(depths_decoder)):
            layer = LSSLayer_up(
                dim=dims_decoder[i_layer],
                depth=depths_decoder[i_layer],
                d_state=d_state,
                drop=drop_rate,
                attn_drop=attn_drop_rate,
                drop_path=dpr_decoder[
                    sum(depths_decoder[:i_layer]) : sum(depths_decoder[: i_layer + 1])
                ],
                norm_layer=norm_layer,
                upsample=PatchExpand2D if (i_layer != 0) else None,
                size=8 * 2 ** (i_layer),
                scan_type=scan_type,
                num_direction=num_direction,
            )
            self.layers_up.append(layer)
        self.apply(self._init_weights)

    def _init_weights(self, m: nn.Module):
        """
        out_proj.weight which is previously initilized in HSSBlock, would be cleared in nn.Linear
        no fc.weight found in the any of the model parameters
        no nn.Embedding found in the any of the model parameters
        so the thing is, HSSBlock initialization is useless

        Conv2D is not intialized !!!
        """
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=0.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    @torch.jit.ignore
    def no_weight_decay(self):
        return {"absolute_pos_embed"}

    @torch.jit.ignore
    def no_weight_decay_keywords(self):
        return {"relative_position_bias_table"}

    def forward(self, x):
        x = rearrange(x, "b c h w -> b h w c")
        out_features = []
        for i, layer in enumerate(self.layers_up):
            x = layer(x)
            if i != 0:
                out_features.insert(0, rearrange(x, "b h w c -> b c h w"))
        return out_features


if __name__ == "__main__":
    # from fvcore.nn import FlopCountAnalysis, flop_count_table, parameter_count
    # vmunet = MambaUPNet([512, 256, 128, 64], [3, 4, 6, 3])
    # bs = 1
    # reso = 8
    # x = torch.randn(bs, 512, reso, reso).cuda()
    # net = vmunet.cuda()
    # net.eval()
    # y = net(x)
    x = torch.randn(25, 4096, 320).cuda()
    cond = torch.randn(25, 1, 32, 1024).cuda()
    self_attention_cond = SS2D_cond(
        d_model=320,
        d_cond=1024,
        cond_size=32,
        dropout=0.1,
        d_state=16,
        size=64,
        scan_type="sweep",
        num_direction=2,
    ).cuda()
    y = self_attention_cond(x, cond)
    # print(y.shape)
