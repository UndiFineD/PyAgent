# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\mongo\client.py
import logging
from typing import Optional

from init.env_variables import DB_URL
from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        self.mongo_uri = DB_URL

    def connect(self) -> Optional[MongoClient]:
        try:
            mongo_client = MongoClient(self.mongo_uri, maxPoolSize=10)
            return mongo_client
        except Exception as e:
            logging.exception(e)
            return None
