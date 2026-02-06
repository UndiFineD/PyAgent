# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\src\lightning\fabric\plugins\collectives\__init__.py
from lightning.fabric.plugins.collectives.collective import Collective
from lightning.fabric.plugins.collectives.single_device import SingleDeviceCollective
from lightning.fabric.plugins.collectives.torch_collective import TorchCollective

__all__ = [
    "Collective",
    "TorchCollective",
    "SingleDeviceCollective",
]
