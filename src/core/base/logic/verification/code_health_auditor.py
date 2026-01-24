
"""
Code health auditor.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from src.core.rust_bridge import RustBridge

from .mixins.stub_detector_mixin import StubDetectorMixin
from .mixins.workspace_auditor_mixin import WorkspaceAuditorMixin


class CodeHealthAuditor(WorkspaceAuditorMixin, StubDetectorMixin):
    """Phase 316: Performs static analysis to detect technical debt and quality issues."""

    def get_code_metrics(self, content: str) -> dict:
        """Phase 318: Returns Rust-accelerated code metrics."""
        return RustBridge.calculate_metrics(content)
