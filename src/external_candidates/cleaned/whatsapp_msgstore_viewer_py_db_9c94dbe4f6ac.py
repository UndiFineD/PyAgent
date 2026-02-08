# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\whatsapp_msgstore_viewer.py\dbs.py\v2.py\db_9c94dbe4f6ac.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\whatsapp-msgstore-viewer\dbs\v2\db.py

#!/usr/bin/env python

# -*- coding: utf-8 -*-


from dbs.abstract_db import AbstractDatabase


class Database(AbstractDatabase):
    def __init__(self, msgstore, wa):

        schema = {
            "chat": {
                "name": "chat",
                "attributes": [
                    "_id",  # chat id
                    "jid_row_id",  # reference to jid table
                    "sort_timestamp",  # timestamp for sorting/display
                    "last_message_row_id",  # last message id in the chat
                ],
            },
            "message": {
                "name": "message",
                "attributes": [
                    "_id",  # message id
                    "chat_row_id",  # chat id reference
                    "key_id",  # key id
                    "from_me",  # sent flag
                    "timestamp",  # message timestamp
                    "text_data",  # message text
                ],
            },
            "message_media": {
                "name": "message_media",
                "attributes": [
                    "message_row_id",  # message reference
                    "file_path",  # media file path
                ],
            },
            "message_quoted": {
                "name": "message_quoted",
                "attributes": [
                    "message_row_id",  # message reference
                    "text_data",  # quoted message text
                    "from_me",  # quoted message from_me flag
                    "key_id",  # quoted message key id
                ],
            },
        }

        super(Database, self).__init__(msgstore, wa, schema=schema)

    def fetch_contact_chats(self):

        sql_query = """

        SELECT 

            chat._id, 

            jid.user,

            jid.raw_string AS raw_string_jid,

            message.text_data, 

            DATETIME(ROUND(chat.sort_timestamp / 1000), 'unixepoch') as timestamp

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

            chat.subject as user,

            jid.raw_string,

            message.text_data, 

            DATETIME(ROUND(chat.sort_timestamp / 1000), 'unixepoch') as timestamp

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

            DATETIME(ROUND(call_log.timestamp / 1000), 'unixepoch') as timestamp, 

            call_log.video_call,

            TIME(call_log.duration, 'unixepoch') as duration,

            jid.user, 

            jid.raw_string as raw_string_jid

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

            DATETIME(ROUND(message.timestamp / 1000), 'unixepoch') as timestamp,  

            IFNULL(message.text_data, '') as text_data,

            message_media.file_path,

            message_quoted.text_data as message_quoted_text_data,

            message_quoted.from_me as message_quoted_from_me,

            message_quoted.key_id as message_quoted_key_id

        FROM message 

        LEFT JOIN message_media ON message._id = message_media.message_row_id

        LEFT JOIN message_quoted ON message._id = message_quoted.message_row_id

        WHERE message.chat_row_id = {chat_id}

        ORDER BY message.timestamp ASC

        """

        return self.msgstore_cursor.execute(sql_query).fetchall()
