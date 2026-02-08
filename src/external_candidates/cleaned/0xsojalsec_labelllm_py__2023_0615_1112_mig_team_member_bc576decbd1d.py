# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\migrations.py\_2023_0615_1112_mig_team_member_bc576decbd1d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\migrations\2023_0615_1112_mig_team_member.py

import sys

sys.path.append(".")

import asyncio

from app.core.config import settings

from app.db.session import mongo_session

from app.schemas.team import TeamMember, TeamMemberRole

from beanie import Document, init_beanie

"""

升级 team 中的用户信息， users_ids: lsit[str] ====> users: list[TeamMember] | None

升级后，不删除 user_ids 字段

升级脚本具有幂等性质，可以多次运行

"""


class Team(Document):
    # 用户 id 列

    users: list[TeamMember] | None

    # 之前的用户列

    user_ids: list[str] | None


async def init_db():
    await init_beanie(
        database=mongo_session[settings.MongoDB_DB_NAME],
        document_models=[Team],  # type: ignore
    )

    teams = await Team.find_all().to_list()

    for team in teams:
        if not team.users:
            team.users = []

            if team.user_ids:
                for v in team.user_ids:
                    team.users.append(TeamMember(user_id=v, role=TeamMemberRole.USER))

            await team.save()  # type: ignore


async def close_db():
    mongo_session.close()


async def mig():
    await init_db()

    await close_db()


if __name__ == "__main__":
    asyncio.run(mig())
