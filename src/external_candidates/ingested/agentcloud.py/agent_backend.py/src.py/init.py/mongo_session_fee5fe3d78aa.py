# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\init\mongo_session.py
from mongo.queries import MongoClientConnection


def start_mongo_session() -> MongoClientConnection:
    return MongoClientConnection()
