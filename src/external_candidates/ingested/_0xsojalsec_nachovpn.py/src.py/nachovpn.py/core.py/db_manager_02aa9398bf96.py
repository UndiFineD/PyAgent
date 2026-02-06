# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\core\db_manager.py
import json
import logging
import sqlite3
import threading
from datetime import datetime


class DBManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.conn = None
        self.lock = threading.Lock()
        self.setup_database()

    def setup_database(self):
        """Initialize the database connection and create tables if they don't exist."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    username TEXT,
                    password TEXT,
                    other TEXT,
                    plugin TEXT
                )
            """)

            self.conn.commit()
            logging.info(f"Database initialized successfully at {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def log_credentials(self, username, password, plugin_name, other_data=None):
        """Log credentials using prepared statements."""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO credentials (username, password, other, plugin) VALUES (?, ?, ?, ?)",
                    (
                        username,
                        password,
                        json.dumps(other_data) if other_data else None,
                        plugin_name,
                    ),
                )
                self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error logging credentials: {e}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            with self.lock:
                self.conn.close()
