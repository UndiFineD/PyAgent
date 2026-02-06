# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-liquid-audio\src\liquid_audio\model\mlp.py
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        hidden_dim: list[int],
        bias: bool = True,
        use_layer_norm: bool = True,
        dropout: float = 0.0,
    ):
        super().__init__()

        channels = [in_channels, *hidden_dim, out_channels]

        layers: list[nn.Module] = []
        if use_layer_norm:
            layers.append(nn.LayerNorm(channels[0]))

        for i in range(len(channels) - 1):
            layers.append(
                nn.Linear(
                    in_features=channels[i],
                    out_features=channels[i + 1],
                    bias=bias,
                )
            )

            if i != (len(channels) - 2):
                layers.append(nn.GELU())
                if dropout > 0:
                    layers.append(nn.Dropout(p=dropout))

        self.model = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)
