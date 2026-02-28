# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OpenBot\policy\openbot\server\__main__.py
from aiohttp import web
from openbot.server.main import app

if __name__ == "__main__":
    web.run_app(app, port=8000)
