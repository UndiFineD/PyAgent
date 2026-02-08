# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\tests.py\unit_tests.py\test_config_object_8cd9f31244b1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\test_config_object.py

from io import StringIO

import pytest

import yaml

from ovo.core.configuration import DEFAULT_OVO_HOME, ConfigProps, OVOConfig

from pydantic_core import ValidationError


def test_config_default():
    data = yaml.safe_load(StringIO(OVOConfig.default(ConfigProps())))

    data["dir"] = DEFAULT_OVO_HOME

    config = OVOConfig(**data)


def test_config_with_extra_args():
    with pytest.raises(ValidationError):
        data = yaml.safe_load(StringIO(OVOConfig.default(ConfigProps())))

        data["dir"] = DEFAULT_OVO_HOME

        data["foo"] = "bar"

        config = OVOConfig(**data)
