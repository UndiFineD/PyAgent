# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\src\lightning\pytorch\demos\__init__.py
from lightning.pytorch.demos.boring_classes import (
    BoringDataModule,
    BoringModel,
    DemoModel,
)
from lightning.pytorch.demos.lstm import LightningLSTM, SequenceSampler, SimpleLSTM
from lightning.pytorch.demos.transformer import (
    LightningTransformer,
    Transformer,
    WikiText2,
)

__all__ = [
    "LightningLSTM",
    "SequenceSampler",
    "SimpleLSTM",
    "LightningTransformer",
    "Transformer",
    "WikiText2",
    "BoringModel",
    "BoringDataModule",
    "DemoModel",
]
