# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mPLUG-DocOwl\UReader\pipeline\trainer.py
import argparse
from functools import partial

import torch
import torch.distributed as dist
from pipeline.utils import batchify
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.distributed import DistributedSampler
from transformers import Trainer


class CustomTrainer(Trainer):

    def get_train_dataloader(self) -> DataLoader:
        dataset = self.train_dataset
        sampler = DistributedSampler(dataset)
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=self._train_batch_size,
            sampler=sampler,
            num_workers=self.args.dataloader_num_workers,
            drop_last=True,
            pin_memory=False,
            collate_fn=batchify,
        )

    def get_eval_dataloader(self, eval_dataset: Dataset | None = None) -> DataLoader:
        dataset = self.eval_dataset
        sampler = DistributedSampler(dataset, shuffle=False)
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=self._train_batch_size,
            sampler=sampler,
            num_workers=self.args.dataloader_num_workers,
            drop_last=True,
            pin_memory=False,
            collate_fn=batchify,
        )
