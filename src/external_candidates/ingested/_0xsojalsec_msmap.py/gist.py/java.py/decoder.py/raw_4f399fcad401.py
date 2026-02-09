# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-msmap\gist\java\decoder\raw.py
code = """
    private byte[] decoder(String payload) {
        return payload.getBytes();
    }
"""

proc = """
            Class base64;
            Object decoder;
            byte[] bytes = payload.getBytes();
"""
