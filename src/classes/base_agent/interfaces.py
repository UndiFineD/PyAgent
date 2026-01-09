#!/usr/bin/env python3

from __future__ import annotations
from typing import Protocol, runtime_checkable, Dict, Any, List, Optional
from pathlib import Path

@runtime_checkable
class AgentInterface(Protocol):
    """
    Core interface for all AI-powered agents. 
    Defining this as a Protocol facilitates future Rust implementation (PyO3).
    """
    file_path: Path
    previous_content: str
    current_content: str

    def read_previous_content(self) -> str: ...
    def improve_content(self, prompt: str) -> str: ...
    def update_file(self) -> bool: ...
    def get_diff(self) -> str: ...
    
    # Advanced features that might be offloaded to Rust later
    def calculate_metrics(self, content: Optional[str] = None) -> Any: ...
    def scan_for_secrets(self, content: str) -> List[str]: ...

@runtime_checkable
class OrchestratorInterface(Protocol):
    """Interface for fleet orchestrators."""
    def execute_task(self, task: str) -> str: ...
    def get_status(self) -> Dict[str, Any]: ...

@runtime_checkable
class CoreInterface(Protocol):
    """Pure logic interface. High-performance, no-IO, candidate for Rust parity."""
    def process_data(self, data: Any) -> Any: ...
    def validate(self, content: str) -> bool: ...
    def get_metadata(self) -> Dict[str, Any]: ...
