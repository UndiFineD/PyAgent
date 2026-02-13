# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LitterBox\app\analyzers\base.py
# app/analyzers/base.py
from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    def __init__(self, config):
        self.config = config
        self.results = {}

    @abstractmethod
    def analyze(self, target):
        """
        Perform the analysis
        :param target: Could be a file path or PID depending on analysis type
        """
        pass

    @abstractmethod
    def cleanup(self):
        """Cleanup after analysis"""
        pass

    def get_results(self):
        return self.results
