# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\service\data\tool.py
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...env import LOG
from ...schema.orm import ToolReference, ToolSOP
from ...schema.result import Result
from ...schema.tool.tool_reference import ToolReferenceData
from ...schema.utils import asUUID


async def rename_tool(db_session: AsyncSession, project_id: asUUID, rename_list: list[tuple[str, str]]) -> Result[None]:
    for old_name, new_name in rename_list:
        tool_ref_query = (
            select(ToolReference).where(ToolReference.project_id == project_id).where(ToolReference.name == old_name)
        )
        result = await db_session.execute(tool_ref_query)
        tool_reference = result.scalars().first()
        if tool_reference is None:
            LOG.warning(f"Tool {old_name} not found")
            continue
        tool_reference.name = new_name
        await db_session.flush()
    return Result.resolve(None)


async def get_tool_names(db_session: AsyncSession, project_id: asUUID) -> Result[List[ToolReferenceData]]:
    # Query to get tool references with SOP count
    tool_ref_query = (
        select(ToolReference.name, func.count(ToolSOP.id).label("sop_count"))
        .outerjoin(ToolSOP, ToolReference.id == ToolSOP.tool_reference_id)
        .where(ToolReference.project_id == project_id)
        .group_by(ToolReference.id, ToolReference.name)
    )

    result = await db_session.execute(tool_ref_query)
    tool_data = result.all()

    return Result.resolve(
        [
            ToolReferenceData(
                name=row.name,
                sop_count=row.sop_count or 0,
            )
            for row in tool_data
        ]
    )
