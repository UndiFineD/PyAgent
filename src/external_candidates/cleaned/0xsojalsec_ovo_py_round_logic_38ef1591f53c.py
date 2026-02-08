# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\logic.py\round_logic_38ef1591f53c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\logic\round_logic.py

from ovo import db, get_username

from ovo.core.database.models import Round


def get_or_create_project_rounds(project_id: str) -> dict[str, Round]:

    project_rounds = db.select(Round, project_id=project_id, order_by="created_date_utc")

    if not project_rounds:
        project_round = Round(project_id=project_id, name="Round 1", author=get_username())

        db.save(project_round)

        project_rounds = [project_round]

    return {r.id: r for r in project_rounds}
