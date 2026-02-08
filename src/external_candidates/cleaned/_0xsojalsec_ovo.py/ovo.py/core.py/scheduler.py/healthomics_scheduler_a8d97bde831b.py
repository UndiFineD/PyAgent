# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\scheduler\healthomics_scheduler.py
import os
import re
from datetime import datetime

from ovo.core.auth import get_username
from ovo.core.aws import AWSSessionManager
from ovo.core.scheduler.base_scheduler import Scheduler, SchedulerTypes
from ovo.core.utils.formatting import format_duration


@SchedulerTypes.register()
class HealthOmicsScheduler(Scheduler):
    def __init__(
        self,
        name: str,
        workdir: str,
        reference_files_dir: str,
        aws: AWSSessionManager,
        allow_submit: bool = True,
        submission_args: dict = None,
    ):
        """
        Args:
            aws:
            name: Human-readable label for this scheduler
            workdir: Working directory - where to store workflow outputs (S3 URI including s3:// prefix)
            reference_files_dir: UNUSED Directory with model weights and other reference files
            role_arn: AWS IAM role ARN
            allow_submit: Whether to allow job submission
            submission_args: Default submission arguments, can be overridden in submit method
        """
        super().__init__(name, workdir, reference_files_dir, allow_submit, submission_args)
        self.aws = aws

    def submit(self, pipeline_name: str, params: dict = None, submission_args: dict = None) -> str:
        """
        Submits a workflow asynchronously and returns the PID.

        :param pipeline_name: Workflow name and revision (ovo.rfdiffusion-end-to-end or github url with @version)
        :param params: Dictionary of parameters to pass to the workflow.
        :param submission_args: Submission arguments for the scheduler, overrides values in self.submission_args
        :return: Scheduler job ID
        """
        assert isinstance(params, dict), f"params should be a dictionary, got: {type(params).__name__}"

        if not self.allow_submit:
            raise RuntimeError("Job submission is disabled")

        submission_args = {**self.submission_args, **(submission_args or {})}
        workflow_name_prefix = submission_args.pop("workflow_name_prefix", "")
        role_arn = submission_args.pop("role_arn", "")

        if re.fullmatch(r"https?://.*", pipeline_name):
            raise NotImplementedError("GitHub URL pipeline names are not supported yet with HealthOmicsScheduler")
        elif "/" in pipeline_name or pipeline_name == "." or pipeline_name.endswith(".nf"):
            raise NotImplementedError("Local path pipeline names are not supported with HealthOmicsScheduler")
        elif "." in pipeline_name:  # custom workflow path (python_module_name.my_workflow)
            module_name, workflow_subpath = pipeline_name.split(".")
        else:
            module_name = "ovo"
            workflow_subpath = pipeline_name

        omics_workflow_name = workflow_name_prefix + module_name + "_" + workflow_subpath
        workflow_id = self.aws.get_latest_workflow_id(workflow_name=omics_workflow_name)

        if submission_args:
            # submission args should be empty at this point
            raise ValueError(f"Unrecognized {type(self).__name__} submission args: {submission_args.keys()}")

        # AWS params
        params = params.copy()
        params["account_id"] = self.aws.get_account_id()
        params["aws_region"] = self.aws.region_name
        params["workflow_bucket"] = self.workdir.replace("s3://", "").split("/")[0]
        params["reference_files_dir"] = "unused"

        username = get_username()

        # Submit the job
        response = self.aws.omics.start_run(
            roleArn=role_arn,
            workflowId=workflow_id,
            workflowType="PRIVATE",
            name=f"OVO {omics_workflow_name} {username}",
            outputUri=f"{self.workdir.rstrip('/')}/{workflow_subpath}/",
            parameters=params,
            storageCapacity=500,
            logLevel="ALL",
            tags={"user": username, "app": "OVO"},
            storageType="STATIC",
        )

        return response["id"]

    def get_status_label(self, job_id: str) -> str:
        """Get human-readable job status label. Should NOT be used to determine job status.

        Can return "Cancelled", "Completed", "Deleted", "Failed", "Pending", "Running", "Starting", "Stopping"
        """
        return self.aws.omics.get_run(id=job_id)["status"].capitalize()

    def get_result(self, job_id: str) -> str | bool | None:
        """Get job result: True if successful, False if failed, None if running."""
        if not isinstance(job_id, str):
            raise ValueError(
                f"Job ID of {type(self).__name__} should be a string, got {job_id} ({type(job_id).__name__}). Make sure to use job_id instead of the DB id."
            )
        status = self.aws.omics.get_run(id=job_id)["status"]
        if status in ["STARTING", "PENDING", "PENDING_REDRIVE", "RUNNING", "STOPPING"]:
            return None
        if status in ["SUCCEEDED", "COMPLETED"]:
            return True
        return False

    def get_log(self, job_id: str) -> str | None:
        """Get job execution full log"""
        if not isinstance(job_id, str):
            raise ValueError(
                f"Job ID of {type(self).__name__} should be a string, got {job_id} ({type(job_id).__name__}). Make sure to use job_id instead of the DB id."
            )
        run = self.aws.omics.get_run(id=job_id)
        # TODO this log file is only available when job is finished
        # We need to read this from CloudWatch instead
        # See logLocation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run.html
        engine_log_s3_uri = os.path.join(run["runOutputUri"], "logs", "engine.log")
        if self.aws.s3_file_exists(engine_log_s3_uri):
            return self.aws.get_s3_bytes(engine_log_s3_uri).decode("utf-8")
        return None

    def cancel(self, job_id):
        """Cancel job execution"""
        raise NotImplementedError()

    def get_output_dir(self, job_id: str) -> str:
        """Get job output path"""
        return os.path.join(self.aws.omics.get_run(id=job_id)["runOutputUri"], "pubdir")

    def get_job_start_time(self, job_id: str) -> datetime | None:
        """Get job start time"""
        run = self.aws.omics.get_run(id=job_id)
        if "startTime" in run:
            return run["startTime"].replace(tzinfo=None)
        return None

    def get_job_stop_time(self, job_id: str) -> datetime | None:
        """Get job end time"""
        run = self.aws.omics.get_run(id=job_id)
        if "stopTime" in run:
            return run["stopTime"].replace(tzinfo=None)
        return None

    def get_startup_time_minutes(self):
        """Get startup time of a task (in minutes)"""
        return 10
