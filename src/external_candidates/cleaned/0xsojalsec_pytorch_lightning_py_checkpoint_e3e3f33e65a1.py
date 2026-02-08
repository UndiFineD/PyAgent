# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pytorch_lightning.py\src.py\lightning.py\pytorch.py\callbacks.py\checkpoint_e3e3f33e65a1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\src\lightning\pytorch\callbacks\checkpoint.py

from lightning.pytorch.callbacks.callback import Callback


class Checkpoint(Callback):
    r"""This is the base class for model checkpointing.

    Expert users may want to subclass it in case of writing custom :class:`~lightning.pytorch.callbacks.Checkpoint`

    callback, so that the trainer recognizes the custom class as a checkpointing callback.

    """
