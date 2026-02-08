# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\absadiki_whatsapp_msgstore_viewer.py\model.py\login_screen_f5fa14965de7.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\absadiki-whatsapp-msgstore-viewer\Model\login_screen.py

from Model.base_model import BaseScreenModel


class LoginScreenModel(BaseScreenModel):
    def __init__(self, base):
        self.base = base

        self._observers = []
