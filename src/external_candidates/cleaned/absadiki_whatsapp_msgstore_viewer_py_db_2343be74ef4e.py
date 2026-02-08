# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\absadiki_whatsapp_msgstore_viewer.py\dbs.py\v3.py\db_2343be74ef4e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\absadiki-whatsapp-msgstore-viewer\dbs\v3\db.py

#!/usr/bin/env python

# -*- coding: utf-8 -*-

from dbs.abstract_db import AbstractDatabase


class Database(AbstractDatabase):
    def __init__(self, msgstore, wa):
        # Updated schema to match the tables/columns present in the provided DDL

        schema = {
            # ------------ chat list ------------
            "chat": {
                "name": "chat",
                "attributes": [
                    "_id",  # Primary key
                    "jid_row_id",  # FK → jid._id
                    "subject",  # Group name (NULL for 1-to-1)
                    "sort_timestamp",  # Sorting timestamp
                    "last_message_row_id",  # FK → message._id
                ],
            },
            # ------------ messages ------------
            "message": {
                "name": "message",
                "attributes": [
                    "_id",  # Primary key
                    "chat_row_id",  # FK → chat._id
                    "key_id",
                    "from_me",
                    "timestamp",
                    "text_data",
                ],
            },
            # ------------ media ------------
            "message_media": {
                "name": "message_media",
                "attributes": ["message_row_id", "file_path"],  # FK → message._id
            },
            # ------------ quoted messages ------------
            "message_quoted": {
                "name": "message_quoted",
                "attributes": [
                    "message_row_id",  # FK → message._id
                    "text_data",
                    "from_me",
                    "key_id",
                ],
            },
            # ------------ call log ------------
            "call_log": {
                "name": "call_log",
                "attributes": [
                    "_id",
                    "jid_row_id",  # FK → jid._id
                    "from_me",
                    "timestamp",
                    "video_call",
                    "duration",
                ],
            },
            # ------------ jid / contacts ------------
            "jid": {"name": "jid", "attributes": ["_id", "user", "raw_string"]},
        }

        super(Database, self).__init__(msgstore, wa, schema=schema)

    # --- fetch_* methods copied from v2 without modification ---

    def fetch_contact_chats(self):
        sql_query = """

        SELECT 

            chat._id, 

            IFNULL(jid.user, '') AS user,

            jid.raw_string AS raw_string_jid,

            message.text_data, 

            DATETIME(ROUND(chat.sort_timestamp / 1000), 'unixepoch') AS timestamp

        FROM chat 

        INNER JOIN jid ON chat.jid_row_id = jid._id

        INNER JOIN message ON chat.last_message_row_id = message._id

        WHERE jid.raw_string NOT LIKE '%g.us'

        ORDER BY timestamp DESC

        """

        return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_group_chats(self):
        sql_query = """

        SELECT 

            chat._id, 

            IFNULL(chat.subject, '') AS user,

            jid.raw_string AS raw_string_jid,

            message.text_data, 

            DATETIME(ROUND(chat.sort_timestamp / 1000), 'unixepoch') AS timestamp

        FROM chat 

        INNER JOIN jid ON chat.jid_row_id = jid._id

        INNER JOIN message ON chat.last_message_row_id = message._id

        WHERE jid.raw_string LIKE '%g.us'

        ORDER BY timestamp DESC

        """

        return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_calls(self, how_many=None):
        sql_query = """

        SELECT 

            call_log._id, 

            call_log.from_me, 

            DATETIME(ROUND(call_log.timestamp / 1000), 'unixepoch') AS timestamp, 

            call_log.video_call,

            TIME(call_log.duration, 'unixepoch') AS duration,

            IFNULL(jid.user, '') AS user, 

            jid.raw_string AS raw_string_jid

        FROM call_log 

        LEFT JOIN jid ON call_log.jid_row_id = jid._id

        """

        if how_many:
            return self.msgstore_cursor.execute(sql_query).fetchmany(how_many)

        else:
            return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_chat(self, chat_id):
        sql_query = f"""

        SELECT  

            message._id, 

            message.key_id, 

            message.from_me, 

            DATETIME(ROUND(message.timestamp / 1000), 'unixepoch') AS timestamp,  

            IFNULL(message.text_data, '') AS text_data,

            message_media.file_path,

            message_quoted.text_data AS message_quoted_text_data,

            message_quoted.from_me AS message_quoted_from_me,

            message_quoted.key_id AS message_quoted_key_id

        FROM message 

        LEFT JOIN message_media ON message._id = message_media.message_row_id

        LEFT JOIN message_quoted ON message._id = message_quoted.message_row_id

        WHERE message.chat_row_id = {chat_id}

        ORDER BY message.timestamp ASC

        """

        return self.msgstore_cursor.execute(sql_query).fetchall()
