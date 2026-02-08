# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\infra.py\agno_aws.py\agno.py\aws.py\resource.py\reference_51bb38cb1f82.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_aws\agno\aws\resource\reference.py

from typing import Optional

from agno.aws.api_client import AwsApiClient


class AwsReference:
    def __init__(self, reference):
        self.reference = reference

    def get_reference(self, aws_client: Optional[AwsApiClient] = None):
        return self.reference(aws_client=aws_client)
