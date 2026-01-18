#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from .mixins.ExecCommandMixin import ExecCommandMixin
from .mixins.ExecIterationMixin import ExecIterationMixin
from .mixins.ExecLoopMixin import ExecLoopMixin


class OrchestratorExecutionMixin(ExecCommandMixin, ExecIterationMixin, ExecLoopMixin):
    """Command execution, git operations, and processing loop methods for OrchestratorAgent."""
