# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-liquid-audio\src\liquid_audio\moshi\quantization\__init__.py
# Copyright (c) Kyutai, all rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""RVQ."""

from .base import BaseQuantizer, DummyQuantizer, QuantizedResult

# flake8: noqa
from .vq import ResidualVectorQuantizer, SplitResidualVectorQuantizer
