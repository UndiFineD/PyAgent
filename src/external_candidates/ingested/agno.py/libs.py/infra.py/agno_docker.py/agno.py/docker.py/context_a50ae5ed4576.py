# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_docker\agno\docker\context.py
from pydantic import BaseModel


class DockerBuildContext(BaseModel):
    network: str
