"""Plugin demonstrating handling of broken imports during agent initialization."""

from src.core.base.BaseAgent import BaseAgent
import non_existent_package_123

class BrokenImportAgent(BaseAgent):
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
