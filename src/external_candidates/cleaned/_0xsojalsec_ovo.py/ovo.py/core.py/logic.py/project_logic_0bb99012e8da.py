# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\logic\project_logic.py
from ovo import db, get_username
from ovo.core.database.models import Project, Round
from sqlalchemy.exc import NoResultFound

PERSONAL_PROJECT_NAME = "Personal project: {author}"


def get_or_create_personal_project() -> Project:
    author = get_username()
    return get_or_create_project(
        PERSONAL_PROJECT_NAME.format(author=author),
        public=False,
        filters=dict(public=False, author=author),
    )


def get_or_create_project(project_name: str, public=False, filters=None) -> Project:
    """Get or create a project by name."""
    author = get_username()
    try:
        return db.get(Project, name=project_name, **(filters or {}))
    except NoResultFound:
        project = Project(name=project_name, public=public, author=author)
        db.save(project)
        return project


def get_or_create_project_round(project_name: str, round_name: str) -> tuple[Project, Round]:
    project = get_or_create_project(project_name)
    try:
        project_round = db.get(Round, name=round_name, project_id=project.id)
    except NoResultFound:
        project_round = Round(name=round_name, project_id=project.id, author=get_username())
        db.save(project_round)
    return project, project_round
