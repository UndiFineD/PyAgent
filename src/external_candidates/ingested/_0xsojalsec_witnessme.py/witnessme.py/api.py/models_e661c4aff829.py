# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-WitnessMe\witnessme\api\models.py
import uuid
from typing import List, Optional, Union

from pydantic import AnyUrl, BaseModel
from witnessme.commands.screenshot import ScanState


class BrowserTasks(BaseModel):
    inputs: int
    execs: int
    pending: int

    class Config:
        orm_mode = True


class ScanConfig(BaseModel):
    target: List[Union[AnyUrl, str]]
    ports: Optional[List[int]] = [80, 8080, 443, 8443]
    threads: Optional[int] = 25
    timeout: Optional[int] = 35


class Scan(BaseModel):
    id: uuid.UUID
    target: List[str]
    ports: List[int]
    threads: int
    timeout: int
    stats: BrowserTasks
    state: ScanState
    report_folder: str

    class Config:
        orm_mode = True
