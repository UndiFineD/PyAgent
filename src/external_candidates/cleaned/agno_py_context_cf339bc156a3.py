# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\infra.py\agno_aws.py\agno.py\aws.py\context_cf339bc156a3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_aws\agno\aws\context.py

from typing import Optional

from pydantic import BaseModel


class AwsBuildContext(BaseModel):
    aws_region: Optional[str] = None

    aws_profile: Optional[str] = None
