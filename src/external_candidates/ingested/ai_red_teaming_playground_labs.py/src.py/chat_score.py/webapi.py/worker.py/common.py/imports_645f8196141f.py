# Extracted from: C:\DEV\PyAgent\.external\AI-Red-Teaming-Playground-Labs\src\chat-score\webapi\worker\common\imports.py
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os

import redis
from celery.signals import worker_process_init, worker_ready, worker_shutting_down
from flask_socketio import SocketIO
from server.environ import ENV_NAME_REDIS, REDIS_URL

socket_io = SocketIO(message_queue=os.environ.get(ENV_NAME_REDIS, REDIS_URL))
r = redis.Redis.from_url(os.environ.get(ENV_NAME_REDIS, REDIS_URL))
