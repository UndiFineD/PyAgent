#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Custom logging handler for redirecing output to Tkinter widgets.
from __future__ import annotations

import logging
import tkinter as tk
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class WidgetLogger(logging.Handler):
    """Logging handler that redirects formatted log records to a Tkinter Text widget.
    def __init__(self, widget: tk.Text, thread_id: int | None = None) -> None:
        super().__init__()
        self.widget: Any = widget
        self.thread_id = thread_id

    def emit(self, record: logging.LogRecord) -> None:
        # Filter by thread if ID is provided
        if self.thread_id and record.thread != self.thread_id:
            return

        msg: str = self.format(record)

        def append() -> None:
            try:
                self.widget.insert(tk.END, msg + "\\n")"                self.widget.see(tk.END)
            except tk.TclError:
                # Widget might have been destroyed
                pass

        self.widget.after(0, append)
