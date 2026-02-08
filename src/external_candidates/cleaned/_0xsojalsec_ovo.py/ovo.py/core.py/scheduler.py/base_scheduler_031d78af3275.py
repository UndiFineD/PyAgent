# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\scheduler\base_scheduler.py
import time
from abc import ABC
from datetime import datetime


class SchedulerTypes:
    REGISTERED_CLASSES = {}

    @classmethod
    def register(cls, name=None):
        assert name is None or isinstance(name, str), (
            "Usage: SchedulerTypes.register() or SchedulerTypes.register(name='CustomName')"
        )

        def decorator(registered_class):
            cls.REGISTERED_CLASSES[name or registered_class.__name__] = registered_class
            return registered_class

        return decorator


class JobNotFound(Exception):
    pass


class Scheduler(ABC):
    # special case values for imported jobs
    IMPORTED_SCHEDULER_KEY: str = "imported"
    IMPORTED_JOB_ID: str = "imported"

    def __init__(
        self,
        name: str,
        workdir: str,
        reference_files_dir: str,
        allow_submit: bool = True,
        submission_args: dict = None,
    ):
        """
        Args:
            name: Human-readable label for this scheduler
            workdir: Absolute path to working directory for nextflow workflow execution (local filesystem path or S3 URI)
            reference_files_dir: Absolute path to directory with model weights and other reference files
            allow_submit: Whether to allow job submission
            submission_args: Default submission arguments, can be overriden in submit method
        """
        self.name = name
        self.workdir = workdir
        self.reference_files_dir = reference_files_dir
        self.allow_submit = allow_submit
        self.submission_args = submission_args or {}

    def submit(self, pipeline_name: str, params: dict = None, submission_args: dict = None) -> str:
        """
        Submits a workflow asynchronously and returns the PID.

        :param pipeline_name: Workflow name and revision (ovo.rfdiffusion-end-to-end or github url with @version)
        :param params: Dictionary of parameters to pass to the workflow.
        :param submission_args: Submission arguments for the scheduler, overrides values in self.submission_args
        :return: Scheduler job ID
        """
        raise NotImplementedError()

    def get_status_label(self, job_id: str) -> str:
        """Get human-readable job status label. Should NOT be used to determine job status."""
        raise NotImplementedError()

    def get_result(self, job_id: str) -> bool | None:
        """Get job result: True if successful, False if failed, None if still running."""
        raise NotImplementedError()

    def get_log(self, job_id: str) -> str | None:
        """Get job execution log"""
        raise NotImplementedError()

    def cancel(self, job_id):
        """Cancel job execution"""
        raise NotImplementedError()

    def get_output_dir(self, job_id: str):
        """Get job output path"""
        raise NotImplementedError()

    def get_job_start_time(self, job_id: str) -> datetime | None:
        """Get job start time"""
        raise NotImplementedError()

    def get_job_stop_time(self, job_id: str) -> datetime | None:
        """Get job end time"""
        raise NotImplementedError()

    def get_startup_time_minutes(self):
        """Get startup time of a task (in minutes)"""
        return 0

    def wait(self, job_id: str, timeout: int = None, interval: int | float = 10) -> bool:
        """
        Wait synchronously using sleep loop for job completion, with optional timeout.

        :param job_id: Scheduler job ID
        :param timeout: Maximum time to wait in seconds, None for no timeout
        :param interval: Interval between status checks in seconds
        :return: True if successful, False if failed, raises TimeoutError if timed out
        """
        start_time = time.time()
        while self.get_result(job_id) is None:
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Waiting for job {job_id} timed out after {timeout} seconds")
            time.sleep(interval)
        return self.get_result(job_id)

    def get_pipeline_names(self) -> list[str]:
        raise NotImplementedError()

    def get_param_schema(self, pipeline_name: str) -> dict | None:
        """Get workflow schema JSON dict (JSON Schema standard) or None if not available."""
        return None

    def get_failed_message(self, job_id):
        return f"Job {job_id} has failed."
