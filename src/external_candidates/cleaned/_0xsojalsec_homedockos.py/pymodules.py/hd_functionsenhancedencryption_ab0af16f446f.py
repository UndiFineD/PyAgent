# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-HomeDockOS\pymodules\hd_FunctionsEnhancedEncryption.py
"""
hd_FunctionsEnhacedEncryption.py
Copyright © 2023-2025 Banshee, All Rights Reserved
https://www.banshee.pro
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
serialized_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)


def get_public_key():
    return public_key


def get_private_key():
    return serialized_private_key
