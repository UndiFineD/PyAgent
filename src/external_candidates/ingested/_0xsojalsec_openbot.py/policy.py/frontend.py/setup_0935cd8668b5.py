# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OpenBot\policy\frontend\setup.py
from setuptools import find_packages, setup

setup(
    name="openbot_frontend",
    version="0.7.0",
    description="OpenBot Frontend package",
    url="https://github.com/sanyatuning/OpenBot",
    author="Balazs Sandor",
    author_email="sanyatuning@gmail.com",
    license="MIT",
    packages=find_packages(include=["openbot_frontend", "openbot_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
