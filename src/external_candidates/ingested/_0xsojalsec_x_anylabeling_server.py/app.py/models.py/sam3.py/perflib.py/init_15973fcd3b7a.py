# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\models\sam3\perflib\__init__.py
# Copyright (c) Meta Platforms, Inc. and affiliates. All Rights Reserved

import os

is_enabled = False
if os.getenv("USE_PERFLIB", "1") == "1":
    # print("Enabled the use of perflib.\n", end="")
    is_enabled = True
