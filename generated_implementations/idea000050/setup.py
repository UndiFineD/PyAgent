"""Setup configuration
"""

from setuptools import find_packages, setup

setup(
    name="idea000050",
    version="0.1.0",
    description="idea-050 - inference-speculative-decoding-runtime",
    author="PyAgent",
    author_email="pyagent@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pytest>=6.0",
        "pytest-cov>=2.10",
    ],
    extras_require={
        "dev": [
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "pytest-mock>=3.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
