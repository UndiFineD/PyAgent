# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\chat-score\webapi\worker\general.py
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from server.keys import REDIS_LOCK_NAME
from server.models.lock import RedisLock
from worker.common.conf import *
from worker.common.imports import *
from worker.tasks.tick import TickTask

lock = RedisLock(r, REDIS_LOCK_NAME)
tick_task = TickTask(r, lock, socket_io)


@worker_ready.connect
def init_worker(**kwargs):
    tick_task.worker_ready(kwargs["sender"].controller.concurrency)


@worker_shutting_down.connect
def stop_worker(**kwargs):
    tick_task.worker_stop()


@celery.task(name="common.tick5s")
def ticks5s():
    tick_task.tick()
