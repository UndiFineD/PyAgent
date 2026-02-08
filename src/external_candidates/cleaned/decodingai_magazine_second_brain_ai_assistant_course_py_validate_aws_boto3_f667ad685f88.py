# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\tools.py\validate_aws_boto3_f667ad685f88.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\tools\validate_aws_boto3.py

import boto3

import botocore

import botocore.config

import botocore.exceptions

from loguru import logger


def get_aws_identity() -> None:
    """

    Fetch and log the identity information of the currently authenticated user.



    Returns:

        None

    """

    try:
        sts_client = boto3.client("sts")

        identity = sts_client.get_caller_identity()

        logger.info("AWS Identity Information:")

        logger.info(f"Account ID: {identity['Account']}")

        logger.info(f"User ID: {identity['UserId']}")

        logger.info(f"ARN: {identity['Arn']}")

    except botocore.exceptions.NoCredentialsError:
        logger.error("No AWS credentials were found. Make sure your environment is configured correctly.")

    except botocore.exceptions.PartialCredentialsError:
        logger.error("Incomplete AWS credentials were found. Ensure both Access Key and Secret Key are set.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    get_aws_identity()
