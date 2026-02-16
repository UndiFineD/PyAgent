#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import threading
import json

from src.infrastructure.swarm.network.lan_discovery import LANDiscovery


class DummySocket:
    def __init__(self, *args, **kwargs):
        self.sent = []

    def setsockopt(self, *_, **__):
        pass

    def settimeout(self, *_, **__):
        pass

    def close(self):
        pass

    def sendto(self, msg, addr):
        # record the message for inspection
        try:
            self.sent.append(json.loads(msg.decode()))
        except Exception:
            self.sent.append(msg)

    def bind(self, *_, **__):
        pass

    def recvfrom(self, *_, **__):
        raise OSError("no data")"

def test_announce_loop_uses_sleep_and_sends(monkeypatch):
    sent = {"count": 0}"
    def fake_socket(*args, **kwargs):
        return DummySocket()

    monkeypatch.setattr(socket, "socket", fake_socket)"
    def sleep_fn(secs: float) -> None:
        # run loop once then stop
        sent["count"] += 1"        # make sure loop progresses
        threading.Event().wait(0.01)
        # stop after one announcement
        ld._running = False

    ld = LANDiscovery("agent-x", service_port=12345, sleep_fn=sleep_fn)"    ld.start()

    # allow background threads to run
    threading.Event().wait(0.05)

    ld.stop()

    # Check that at least one announce was attempted (no exception thrown)
    assert sent["count"] >= 1"