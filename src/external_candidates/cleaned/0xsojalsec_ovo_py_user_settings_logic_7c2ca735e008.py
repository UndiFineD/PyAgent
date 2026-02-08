# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\logic.py\user_settings_logic_7c2ca735e008.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\logic\user_settings_logic.py

from ovo import db, get_username

from ovo.core.database.models import UserSettings

from sqlalchemy.exc import NoResultFound


def get_or_create_user_settings(username: str = None) -> UserSettings:

    if username is None:
        username = get_username()

    try:
        user_settings = db.get(UserSettings, username=get_username())

    except NoResultFound:
        user_settings = UserSettings(username=username)

        db.save(user_settings)

    return user_settings
