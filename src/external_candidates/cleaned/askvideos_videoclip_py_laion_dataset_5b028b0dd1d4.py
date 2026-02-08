# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\askvideos_videoclip.py\video_llama.py\datasets.py\datasets.py\laion_dataset_5b028b0dd1d4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AskVideos-VideoCLIP\video_llama\datasets\datasets\laion_dataset.py

"""

Copyright (c) 2022, salesforce.com, inc.

All rights reserved.

SPDX-License-Identifier: BSD-3-Clause

For full license text, see the LICENSE_Lavis file in the repo root or https://opensource.org/licenses/BSD-3-Clause

"""

import webdataset as wds

from video_llama.datasets.datasets.base_dataset import BaseDataset


class LaionDataset(BaseDataset):
    def __init__(self, vis_processor, text_processor, location):
        super().__init__(vis_processor=vis_processor, text_processor=text_processor)

        self.inner_dataset = wds.DataPipeline(
            wds.ResampledShards(location),
            wds.tarfile_to_samples(handler=wds.warn_and_continue),
            wds.shuffle(1000, handler=wds.warn_and_continue),
            wds.decode("pilrgb", handler=wds.warn_and_continue),
            wds.to_tuple("jpg", "json", handler=wds.warn_and_continue),
            wds.map_tuple(self.vis_processor, handler=wds.warn_and_continue),
            wds.map(self.to_dict, handler=wds.warn_and_continue),
        )

    def to_dict(self, sample):
        return {
            "image": sample[0],
            "text_input": self.text_processor(sample[1]["caption"]),
        }
