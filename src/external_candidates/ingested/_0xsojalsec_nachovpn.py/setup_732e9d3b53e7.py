# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\setup.py
from setuptools import find_packages, setup

setup(
    name="nachovpn",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "cryptography==42.0.5",
        "jinja2>=3.0.0",
        "scapy>=2.5.0",
        "requests>=2.31.0",
        "flask>=3.0.2",
        "cabarchive>=0.2.4",
        "pycryptodome>=3.20.0",
    ],
    python_requires=">=3.9",
    description="A tasty, but malicious SSL-VPN server",
    entry_points={
        "console_scripts": [
            "nachovpn=nachovpn.server:main",
        ],
    },
)
