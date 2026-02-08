# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\service\data\session.py
from ...infra.db import AsyncSession
from ...schema.orm import Session
from ...schema.result import Result
from ...schema.utils import asUUID


async def fetch_session(db_session: AsyncSession, session_id: asUUID) -> Result[Session]:
    session = await db_session.get(Session, session_id)
    if session is None:
        return Result.reject(f"Session {session_id} not found")
    return Result.resolve(session)
