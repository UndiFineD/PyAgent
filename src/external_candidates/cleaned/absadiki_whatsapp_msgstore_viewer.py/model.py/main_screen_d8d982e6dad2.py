# Extracted from: C:\DEV\PyAgent\.external\absadiki-whatsapp-msgstore-viewer\Model\main_screen.py
from dbs.abstract_db import AbstractDatabase
from Model.base_model import BaseScreenModel


class MainScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """

    def __init__(self, base):
        self.base: AbstractDatabase = base

    def set_base(self, base):
        self.base = base

    def get_contact_chats(self):
        contact_chat_list = self.base.fetch_contact_chats()
        if self.base.contacts is not None:
            for contact_chat in contact_chat_list:
                raw_jid = contact_chat.get("raw_string_jid")
                if raw_jid in self.base.contacts:
                    display_name = self.base.contacts[raw_jid].get("display_name", "")
                    if display_name:
                        contact_chat["user"] = f"{display_name} <{contact_chat['user']}>"
                    else:
                        contact_chat["user"] = f"{contact_chat['user']}"
                else:
                    print(f"Contact {raw_jid} does not exist")
        return contact_chat_list

    def get_group_chats(self):
        group_chat_list = self.base.fetch_group_chats()
        return group_chat_list

    def get_calls(self, how_many=None):
        calls = self.base.fetch_calls(how_many)
        if self.base.contacts is not None:
            # users with their display names
            for call in calls:
                try:
                    call["user"] = self.base.contacts[call["raw_string"]]["display_name"] + f" <{call['user']}> "

                except KeyError:
                    pass  # already mentioned

        return calls

    def get_status(self, jid):
        try:
            st = self.base.contacts[jid]["status"]
            if st is not None:
                return st
            else:
                raise KeyError
        except Exception:
            return "<No Status>"
