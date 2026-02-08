# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_red_teaming_playground_labs.py\src.py\chat_score.py\webapi.py\worker.py\common.py\base_a9a6c3f92bcc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\chat-score\webapi\worker\common\base.py

# Copyright (c) Microsoft Corporation.

# Licensed under the MIT License.

from abc import abstractmethod

class BaseTask:

    @abstractmethod

    def worker_ready(self, concurrency: int):

        pass

    @abstractmethod

    def worker_stop(self):

        pass

