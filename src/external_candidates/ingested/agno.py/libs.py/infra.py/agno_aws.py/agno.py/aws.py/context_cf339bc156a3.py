# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_aws\agno\aws\context.py
from typing import Optional

from pydantic import BaseModel


class AwsBuildContext(BaseModel):
    aws_region: Optional[str] = None
    aws_profile: Optional[str] = None
