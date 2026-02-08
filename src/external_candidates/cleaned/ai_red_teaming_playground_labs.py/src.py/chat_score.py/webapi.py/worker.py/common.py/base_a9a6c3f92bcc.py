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
