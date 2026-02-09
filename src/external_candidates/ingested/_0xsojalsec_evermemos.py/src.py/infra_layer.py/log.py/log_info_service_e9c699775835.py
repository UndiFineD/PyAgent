# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\infra_layer\log\log_info_service.py
"""
Log information service

Provides injection and management of log context information, supporting asynchronous context manager pattern.
Mainly handles:
- trace_id: Request trace ID
- group_id: Group ID
- user_id: User ID
"""

from contextlib import asynccontextmanager
from typing import Optional

from core.context import context
from core.di.decorators import component
from core.di.utils import get_bean_by_type
from core.observation.logger import get_logger

logger = get_logger(__name__)


@component(name="log_info_service")
class LogInfoService:
    """Log information service responsible for managing and injecting log-related context information

    Uses @component decorator to ensure singleton pattern, can be injected into other components via DI system.
    """

    @asynccontextmanager
    async def inject_log_info(
        self,
        trace_id: Optional[str] = None,
        group_id: Optional[str] = None,
        from_user_id: Optional[str] = None,
    ):
        """
        Async context manager to inject log information into context

        Args:
            trace_id: Trace ID, auto-generated if not provided
            group_id: Group ID
            from_user_id: Initiator ID

        Yields:
            Dictionary of injected context information
        """
        # Get current app_info and create a new copy
        current_app_info = context.get_current_app_info() or {}
        app_info = current_app_info.copy()

        try:
            # Update values in the new dictionary
            if trace_id is not None:
                app_info["trace_id"] = trace_id
            # Update group_id and from_user_id (if new values are provided)
            if group_id is not None:
                app_info["group_id"] = group_id
            if from_user_id is not None:
                app_info["from_user_id"] = from_user_id

            # Set the updated app_info
            token = context.set_current_app_info(app_info)

            try:
                # Return the injected context information
                yield app_info
            finally:
                # Use token to restore to original state
                context.clear_current_app_info(token)

        except Exception as e:
            logger.error("Error occurred while injecting log information: %s", e)
            raise

    @asynccontextmanager
    async def override_trace_id(self, trace_id: str):
        """
        Async context manager to temporarily override trace_id

        Args:
            trace_id: New trace ID

        Yields:
            Updated context information dictionary
        """
        async with self.inject_log_info(trace_id=trace_id):
            yield

    @asynccontextmanager
    async def override_group_id(self, group_id: str):
        """
        Async context manager to temporarily override group_id

        Args:
            group_id: New group ID

        Yields:
            Updated context information dictionary
        """
        async with self.inject_log_info(group_id=group_id):
            yield

    @asynccontextmanager
    async def override_from_user_id(self, from_user_id: str):
        """
        Async context manager to temporarily override from_user_id

        Args:
            from_user_id: New initiator ID

        Yields:
            Updated context information dictionary
        """
        async with self.inject_log_info(from_user_id=from_user_id):
            yield

    @staticmethod
    def get_current_trace_id() -> Optional[str]:
        """Get current trace_id"""
        app_info = context.get_current_app_info()
        return app_info.get("trace_id") if app_info else None

    @staticmethod
    def get_current_group_id() -> Optional[str]:
        """Get current group_id"""
        app_info = context.get_current_app_info()
        return app_info.get("group_id") if app_info else None

    @staticmethod
    def get_current_from_user_id() -> Optional[str]:
        """Get current initiator ID"""
        app_info = context.get_current_app_info()
        return app_info.get("from_user_id") if app_info else None


# Global log service instance
_log_service: Optional[LogInfoService] = None


def get_log_service() -> LogInfoService:
    """Get global log service instance"""
    global _log_service
    if _log_service is None:
        _log_service = get_bean_by_type(LogInfoService)
    return _log_service


@asynccontextmanager
async def log_context(
    *,
    trace_id: Optional[str] = None,
    group_id: Optional[str] = None,
    from_user_id: Optional[str] = None,
):
    """
    Unified log context manager

    Example:
        async with log_context(trace_id="123", group_id="456"):
            await some_operation()
    """
    async with get_log_service().inject_log_info(
        trace_id=trace_id, group_id=group_id, from_user_id=from_user_id
    ) as app_info:
        yield app_info


# Export convenience functions
get_current_from_user_id = LogInfoService.get_current_from_user_id
get_current_group_id = LogInfoService.get_current_group_id
get_current_trace_id = LogInfoService.get_current_trace_id
