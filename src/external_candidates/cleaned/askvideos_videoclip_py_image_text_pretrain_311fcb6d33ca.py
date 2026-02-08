# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\askvideos_videoclip.py\video_llama.py\tasks.py\image_text_pretrain_311fcb6d33ca.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AskVideos-VideoCLIP\video_llama\tasks\image_text_pretrain.py

"""

Copyright (c) 2022, salesforce.com, inc.

All rights reserved.

SPDX-License-Identifier: BSD-3-Clause

For full license text, see the LICENSE_Lavis file in the repo root or https://opensource.org/licenses/BSD-3-Clause

"""

from video_llama.common.registry import registry

from video_llama.tasks.base_task import BaseTask

@registry.register_task("image_text_pretrain")

class ImageTextPretrainTask(BaseTask):

    def __init__(self):

        super().__init__()

    def evaluation(self, model, data_loader, cuda_enabled=True):

        pass

