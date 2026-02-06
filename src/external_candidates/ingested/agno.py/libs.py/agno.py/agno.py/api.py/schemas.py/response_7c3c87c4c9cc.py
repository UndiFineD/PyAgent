# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\api\schemas\response.py
from pydantic import BaseModel


class ApiResponseSchema(BaseModel):
    status: str = "fail"
    message: str = "invalid request"
