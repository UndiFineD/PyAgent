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

    def read_previous_content(self) -> str:
        raise NotImplementedError()
    def improve_content(self, prompt: str) -> str:
        raise NotImplementedError()
    def update_file(self) -> bool:
        raise NotImplementedError()
    def get_diff(self) -> str:
        raise NotImplementedError()
    
    # Advanced features that might be offloaded to Rust later
    def calculate_metrics(self, content: Optional[str] = None) -> Any:
        raise NotImplementedError()
    def scan_for_secrets(self, content: str) -> List[str]:
        raise NotImplementedError()

@runtime_checkable
class OrchestratorInterface(Protocol):
    """Interface for fleet orchestrators."""
    def execute_task(self, task: str) -> str:
        raise NotImplementedError()
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError()

@runtime_checkable
class CoreInterface(Protocol):
    """Pure logic interface. High-performance, no-IO, candidate for Rust parity."""
    def process_data(self, data: Any) -> Any:
        raise NotImplementedError()
    def validate(self, content: str) -> bool:
        raise NotImplementedError()
    def get_metadata(self) -> Dict[str, Any]:
        raise NotImplementedError()

@runtime_checkable
class ContextRecorderInterface(Protocol):
    """Interface for cognitive recording and context harvesting."""
    def record_interaction(self, provider: str, model: str, prompt: str, result: str, meta: Dict[str, Any] = None) -> None:
        raise NotImplementedError()
