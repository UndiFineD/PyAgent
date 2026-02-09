# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\api\v1\endpoints\operator\__init__.py
from app.api import deps
from fastapi import APIRouter, Depends

from . import label_task, label_task_stat

router = APIRouter(
    prefix="/operator",
    tags=["operator"],
    dependencies=[Depends(deps.is_admin_or_operator)],
)
router.include_router(label_task.router)
router.include_router(label_task_stat.router)
