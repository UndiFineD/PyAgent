#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\third_party\Matcha-TTS\setup.py
#!/usr/bin/env python
import os

import numpy
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

exts = [
    Extension(
        name="matcha.utils.monotonic_align.core",
        sources=["matcha/utils/monotonic_align/core.pyx"],
    )
]

with open("README.md", encoding="utf-8") as readme_file:
    README = readme_file.read()

cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "matcha", "VERSION")) as fin:
    version = fin.read().strip()

setup(
    name="matcha-tts",
    version=version,
    description="🍵 Matcha-TTS: A fast TTS architecture with conditional flow matching",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Shivam Mehta",
    author_email="shivam.mehta25@gmail.com",
    url="https://shivammehta25.github.io/Matcha-TTS",
    install_requires=[
        str(r)
        for r in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
    ],
    include_dirs=[numpy.get_include()],
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests/*", "examples", "examples/*"]),
    # use this to customize global commands available in the terminal after installing the package
    entry_points={
        "console_scripts": [
            "matcha-data-stats=matcha.utils.generate_data_statistics:main",
            "matcha-tts=matcha.cli:cli",
            "matcha-tts-app=matcha.app:main",
        ]
    },
    ext_modules=cythonize(exts, language_level=3),
    python_requires=">=3.9.0",
)
