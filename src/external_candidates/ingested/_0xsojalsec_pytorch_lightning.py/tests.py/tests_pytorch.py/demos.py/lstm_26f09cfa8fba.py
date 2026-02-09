# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\tests_pytorch\demos\lstm.py
from lightning.pytorch.demos.lstm import SequenceSampler


def test_sequence_sampler():
    dataset = list(range(103))
    sampler = SequenceSampler(dataset, batch_size=4)
    assert len(sampler) == 25
    batches = list(sampler)
    assert batches[0] == [0, 25, 50, 75]
    assert batches[1] == [1, 26, 51, 76]
    assert batches[24] == [24, 49, 74, 99]
