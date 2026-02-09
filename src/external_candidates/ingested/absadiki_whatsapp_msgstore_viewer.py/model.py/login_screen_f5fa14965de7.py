# Extracted from: C:\DEV\PyAgent\.external\absadiki-whatsapp-msgstore-viewer\Model\login_screen.py
from Model.base_model import BaseScreenModel


class LoginScreenModel(BaseScreenModel):
    def __init__(self, base):
        self.base = base
        self._observers = []
