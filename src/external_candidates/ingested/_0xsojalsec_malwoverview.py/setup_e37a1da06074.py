# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-malwoverview\setup.py
#!/usr/bin/env python3
import os
import platform
from pathlib import Path

from setuptools import find_packages, setup

USER_HOME_DIR = str(Path.home()) + os.sep

with open("README.md", encoding="utf8") as readme:
    long_description = readme.read()

setup(
    name="malwoverview",
    version="6.2",
    author="Alexandre Borges",
    author_email="reverseexploit@proton.me",
    license="GNU GPL v3.0",
    url="https://github.com/alexandreborges/malwoverview",
    description=("Malwoverview is a first response tool for threat hunting."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "pefile",
        "colorama",
        "python-magic; platform_system == 'Linux' or platform_system == 'Darwin'",
        "simplejson",
        "requests",
        "validators",
        "geocoder",
        "polyswarm-api",
        "pathlib",
        "configparser",
        "python-magic-bin; platform_system == 'Windows'",
    ],
    entry_points={
        "console_scripts": [
            "malwoverview = malwoverview.malwoverview:main",
        ]
    },
    package_data={"": ["README.md, LICENSE, .malwapi.conf"]},
    data_files=[(USER_HOME_DIR, [".malwapi.conf"])],
)
