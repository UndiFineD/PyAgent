# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\askvideos_videoclip.py\video_llama.py\tasks.py\video_text_pretrain_217ce39a933d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AskVideos-VideoCLIP\video_llama\tasks\video_text_pretrain.py

"""

Copyright (c) 2022, salesforce.com, inc.

All rights reserved.

SPDX-License-Identifier: BSD-3-Clause

For full license text, see the LICENSE_Lavis file in the repo root or https://opensource.org/licenses/BSD-3-Clause

"""

from video_llama.common.registry import registry

from video_llama.tasks.base_task import BaseTask

@registry.register_task("video_text_pretrain")

class VideoTextPretrainTask(BaseTask):

    def __init__(self):

        super().__init__()

    def evaluation(self, model, data_loader, cuda_enabled=True):

        pass

