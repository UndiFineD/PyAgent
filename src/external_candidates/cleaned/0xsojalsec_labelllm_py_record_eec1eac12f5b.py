# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\schemas.py\record_eec1eac12f5b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\schemas\record.py

from enum import Enum

from app.schemas.data import DoDataBase

from app.schemas.evaluation import Evaluation

from pydantic import BaseModel, Field


class RecordStatus(str, Enum):
    """

    数据状态

    """

    # 加工中

    PROCESSING = "processing"

    # 已完成

    COMPLETED = "completed"

    # 已废弃

    DISCARDED = "discarded"


class RecordFullStatus(str, Enum):
    """

    数据状态

    """

    # 加工中

    PROCESSING = "processing"

    # 已完成

    COMPLETED = "completed"

    # 已废弃

    DISCARDED = "discarded"

    # 审核通过

    APPROVED = "approved"

    # 审核未通过

    REJECTED = "rejected"

    # 无效问卷

    INVALID = "invalid"


class ViewGroupUser(BaseModel):
    user_id: str = Field(description="用户id", alias="_id")

    completed_data_count: int = Field(description="答题数")

    discarded_data_count: int = Field(description="未达标题数")


class DoRecord(DoDataBase):
    """

    数据信息

    """

    flow_index: int = 1

    creator_id: str

    create_time: int

    submit_time: int

    evaluation: Evaluation

    status: RecordStatus
