# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pytorch_lightning.py\tests.py\tests_fabric.py\helpers.py\datasets_8ea03986bea4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\tests_fabric\helpers\datasets.py

from collections.abc import Iterator

import torch

from torch import Tensor

from torch.utils.data import Dataset, IterableDataset


class RandomDataset(Dataset):
    def __init__(self, size: int, length: int) -> None:
        self.len = length

        self.data = torch.randn(length, size)

    def __getitem__(self, index: int) -> Tensor:
        return self.data[index]

    def __len__(self) -> int:
        return self.len


class RandomIterableDataset(IterableDataset):
    def __init__(self, size: int, count: int) -> None:
        self.count = count

        self.size = size

    def __iter__(self) -> Iterator[Tensor]:
        for _ in range(self.count):
            yield torch.randn(self.size)
