from src.classes.base_agent import BaseAgent
import non_existent_package_123

class BrokenImportAgent(BaseAgent):
    def __init__(self, file_path):
        super().__init__(file_path)
