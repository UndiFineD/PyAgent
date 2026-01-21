#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from .mixins.exec_command_mixin import ExecCommandMixin
from .mixins.exec_iteration_mixin import ExecIterationMixin
from .mixins.exec_loop_mixin import ExecLoopMixin


class OrchestratorExecutionMixin(ExecCommandMixin, ExecIterationMixin, ExecLoopMixin):
    """Command execution, git operations, and processing loop methods for OrchestratorAgent."""
