# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\chocomintx.py\xiaohongshutools.py\scripts.py\units.py\fuck_reverse_crypto.py\hash_functions_2f11adf4b81b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\units\fuck_reverse_crypto\hash_functions.py

import hashlib

import zlib


def md5_encode(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


def sha256_encode(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def sha1_encode(data: str) -> str:
    return hashlib.sha1(data.encode()).hexdigest()


def sha256_encode(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def crc32_encode(data: str) -> str:
    return zlib.crc32(data.encode())
