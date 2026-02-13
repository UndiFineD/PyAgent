# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\Listeners\HTTP\database\db.py
from flask_mongoengine import MongoEngine

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
