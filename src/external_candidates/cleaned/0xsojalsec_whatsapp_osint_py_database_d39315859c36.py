# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whatsapp_osint.py\utils.py\database_d39315859c36.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whatsapp-osint\utils\database.py

import sqlite3


class Database:
    def create_table():
        conn = sqlite3.connect("database/database.db")

        c = conn.cursor()

        c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Connections'")

        table_exists = c.fetchone()[0]

        if not table_exists:
            c.execute(
                "CREATE TABLE Connections (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, date TEXT, hour TEXT, minute TEXT, second TEXT, type_connection TEXT, time_connected TEXT)"
            )

        conn.commit()

        conn.close()

    def insert_connection_data(name, date, hour, minute, second, type_connection):
        conn = sqlite3.connect("database/database.db")

        c = conn.cursor()

        c.execute(
            "INSERT INTO Connections (user_name, date, hour, minute, second, type_connection) VALUES (?, ?, ?, ?, ?, ?)",
            (name, date, hour, minute, second, type_connection),
        )

        conn.commit()

        conn.close()

    def insert_disconnection_data(name, date, hour, minute, second, type_connection, time_connected):
        conn = sqlite3.connect("database/database.db")

        c = conn.cursor()

        c.execute(
            "INSERT INTO Connections (user_name, date, hour, minute, second, type_connection, time_connected) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, date, hour, minute, second, type_connection, time_connected),
        )

        conn.commit()

        conn.close()
