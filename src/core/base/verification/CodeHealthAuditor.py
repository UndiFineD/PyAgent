# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from .mixins.WorkspaceAuditorMixin import WorkspaceAuditorMixin
from .mixins.StubDetectorMixin import StubDetectorMixin

from src.core.rust_bridge import RustBridge

class CodeHealthAuditor(WorkspaceAuditorMixin, StubDetectorMixin):
    """Phase 316: Performs static analysis to detect technical debt and quality issues."""
    
    def get_code_metrics(self, content: str) -> dict:
        """Phase 318: Returns Rust-accelerated code metrics."""
        return RustBridge.calculate_metrics(content)
