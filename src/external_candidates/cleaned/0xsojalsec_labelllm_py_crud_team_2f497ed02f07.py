# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\crud.py\crud_team_2f497ed02f07.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\crud\crud_team.py

from typing import Any

from uuid import UUID

from app.crud.base import CRUDBase

from app.models.team import Team, TeamCreate, TeamUpdate

from beanie.operators import Eq, In, RegEx


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def query(
        self,
        *,
        _id: list[Any] | Any = None,
        skip: int | None = None,
        limit: int | None = None,
        sort: str | list[str] | None = None,
        user_id: list[str] | str | None = None,
        team_id: list[UUID] | UUID | None = None,
        name: str | None = None,
    ):
        query = super().query(_id=_id, skip=skip, limit=limit, sort=sort)

        if user_id is not None:
            if isinstance(user_id, list):
                query = query.find(In("users.user_id", user_id))

            else:
                query = query.find(Eq("users.user_id", user_id))

        if team_id is not None:
            if isinstance(team_id, list):
                query = query.find(In(self.model.team_id, team_id))

            else:
                query = query.find(self.model.team_id == team_id)

        if name is not None:
            query = query.find(RegEx(field=self.model.name, pattern=name))  # type: ignore

        return query


team = CRUDTeam(Team)
