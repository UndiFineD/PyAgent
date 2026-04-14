"""Observability Module - Logging, Metrics, Tracing
"""

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

@dataclass
class Metric:
    """Metric data structure"""

    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)

    def __repr__(self):
        return f"Metric(name={self.name}, value={self.value}, tags={self.tags})"

class MetricsCollector:
    """Collect and aggregate metrics"""

    def __init__(self):
        self.metrics: Dict[str, list] = {}
        self.logger = logging.getLogger(__name__)

    def record(self, metric: Metric):
        """Record a metric"""
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)
        self.logger.debug(f"Recorded: {metric}")

    def get_metrics(self, name: Optional[str] = None) -> Dict[str, list]:
        """Get recorded metrics"""
        if name:
            return {name: self.metrics.get(name, [])}
        return self.metrics

    def clear(self):
        """Clear all metrics"""
        self.metrics.clear()

class LoggerFactory:
    """Factory for creating configured loggers"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.loggers = {}
        self._initialized = True

    def get_logger(self, name: str, level: LogLevel = LogLevel.INFO) -> logging.Logger:
        """Get or create a logger"""
        if name not in self.loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level.value)

            # Create console handler
            handler = logging.StreamHandler()
            handler.setLevel(level.value)

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            self.loggers[name] = logger

        return self.loggers[name]

@contextmanager
def trace_execution(operation_name: str, logger: Optional[logging.Logger] = None):
    """Context manager for tracing operation execution"""
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = time.time()
    logger.info(f"Starting: {operation_name}")

    try:
        yield
        duration = time.time() - start_time
        logger.info(f"Completed: {operation_name} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Failed: {operation_name} ({duration:.2f}s) - {e}")
        raise

def initialize():
    """Initialize observability system"""
    logger = LoggerFactory().get_logger(__name__)
    logger.info("Observability system initialized")

def execute():
    """Execute observability"""
    return {"status": "observability_active", "metrics": "collecting"}

def shutdown():
    """Shutdown observability"""
    logger = LoggerFactory().get_logger(__name__)
    logger.info("Observability system shutdown")
