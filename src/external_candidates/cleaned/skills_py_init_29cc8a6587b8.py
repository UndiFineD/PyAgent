# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\chocomintx.py\xiaohongshutools.py\scripts.py\request.py\web.py\apis.py\init_29cc8a6587b8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\request\web\apis\__init__.py

from .auth import Authentication

from .comments import Comments

from .note import Note

from .user import User


class APIModule:
    def __init__(self, __session):
        self.auth = Authentication(__session)

        self.comments = Comments(__session)

        self.note = Note(__session)

        self.user = User(__session)
