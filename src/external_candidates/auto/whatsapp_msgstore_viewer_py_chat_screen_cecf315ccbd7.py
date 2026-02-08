# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\whatsapp_msgstore_viewer.py\model.py\chat_screen_cecf315ccbd7.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\whatsapp-msgstore-viewer\Model\chat_screen.py

from dbs.abstract_db import AbstractDatabase

from Model.base_model import BaseScreenModel

class ChatScreenModel(BaseScreenModel):

    """

    Implements the logic of the

    :class:`~View.main_screen.ChatScreen.ChatScreenView` class.

    """

    def __init__(self, base):

        self.base: AbstractDatabase = base

    def get_chat(self, chat_id):

        return self.base.fetch_chat(chat_id)

