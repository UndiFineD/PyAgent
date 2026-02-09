# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-HomeDockOS\pymodules\hd_NonceGenerator.py
"""
hd_NonceGen.py
Copyright © 2023-2025 Banshee, All Rights Reserved
https://www.banshee.pro
"""

import base64
import os

from flask import g


def generate_nonce():
    return base64.b64encode(os.urandom(32)).decode("utf-8")


def setup_nonce(app):
    @app.before_request
    def set_nonce():
        g.nonce = generate_nonce()
