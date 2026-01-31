#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import socket
import threading

from src.infrastructure.swarm.network.network_utils import wait_for_port


def test_wait_for_port_detects_open_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    addr, port = s.getsockname()
    s.listen(1)

    try:
        ok = wait_for_port("127.0.0.1", port, timeout=1.0, poll_interval=0.01)
        assert ok is True
    finally:
        s.close()


def test_wait_for_port_times_out_on_closed_port():
    # Pick a high-numbered port that is likely unused
    ok = wait_for_port("127.0.0.1", 59999, timeout=0.1, poll_interval=0.01)
    assert ok is False
