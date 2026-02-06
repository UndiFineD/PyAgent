# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\steps\infrastructure\upload_to_s3.py
from pathlib import Path

from second_brain_offline.config import settings
from second_brain_offline.infrastructure.aws.s3 import S3Client
from typing_extensions import Annotated
from zenml import get_step_context, step


@step
def upload_to_s3(
    folder_path: Path,
    s3_prefix: str = "",
) -> Annotated[str, "output"]:
    s3_client = S3Client(bucket_name=settings.AWS_S3_BUCKET_NAME)
    s3_client.upload_folder(local_path=folder_path, s3_prefix=s3_prefix)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="output",
        metadata={
            "folder_path": str(folder_path),
            "s3_prefix": s3_prefix,
        },
    )

    return str(folder_path)
