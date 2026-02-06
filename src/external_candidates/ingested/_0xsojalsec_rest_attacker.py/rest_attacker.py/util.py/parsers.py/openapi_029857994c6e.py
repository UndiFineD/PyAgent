# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-REST-Attacker\rest_attacker\util\parsers\openapi.py
# Copyright (C) 2021-2022 the REST-Attacker authors. See COPYING and CONTRIBUTORS.md for legal info.

"""
Parses an OpenAPI file. OpenAPI files are distributed as YAML
or JSON files.
"""

import json
import logging
from pathlib import Path

import yaml
from rest_attacker.util.openapi.wrapper import OpenAPI


def load_openapi(description_id: str, path: Path):
    """
    Load an OpenAPI YAML or JSON definition.

    :param description_id: Identifier for the description.
    :type description_id: str
    :param path: Path to the file.
    :type path: pathlib.Path
    """
    if not path.is_file():
        raise Exception(f"{path} is not a file")

    with path.open() as apifile:
        logging.debug(f"Loading OpenAPI description at: {path}")
        if path.suffix == ".json":
            return OpenAPI(description_id, json.load(apifile))

        elif path.suffix == ".yaml":
            return OpenAPI(
                description_id, yaml.load(apifile, Loader=yaml.loader.FullLoader)
            )

        else:
            raise Exception(
                (
                    f"{path.suffix} is not a recognized extension. "
                    "Expected '.json' or '.yaml'"
                )
            )
