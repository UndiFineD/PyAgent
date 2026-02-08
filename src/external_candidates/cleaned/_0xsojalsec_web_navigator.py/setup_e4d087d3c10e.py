# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\setup.py
from setuptools import find_packages, setup

with open("./docs/README.md") as f:
    long_description = f.read()
setup(
    name="Web-Agent",
    version="0.1",
    description="The web agent is designed to automate the process of gathering information from the internet, such as to navigate websites, perform searches, and retrieve data.",
    author="jeomon",
    author_email="jeogeoalukka@gmail",
    url="https://github.com/Jeomon/Web-Agent",
    packages=find_packages(),
    install_requires=[
        "langgraph",
        "tenacityrequestsplaywrighttermcolorpython-dotenvhttpxnest_asyncioMainContentExtractor",
    ],
    entry_points={"console_scripts": ["web-agent=main:main"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
)
