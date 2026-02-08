# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pytorch_lightning.py\tests.py\tests_fabric.py\plugins.py\collectives.py\test_single_device_e7073c48e393.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\tests_fabric\plugins\collectives\test_single_device.py

from unittest import mock

import pytest

from lightning.fabric.plugins.collectives import SingleDeviceCollective


def test_can_instantiate_without_args():

    SingleDeviceCollective()


def test_create_group():

    collective = SingleDeviceCollective()

    assert collective.is_initialized()

    with pytest.raises(RuntimeError, match=r"SingleDeviceCollective` does not own a group"):
        _ = collective.group

    with mock.patch("lightning.fabric.plugins.collectives.single_device.SingleDeviceCollective.new_group") as new_mock:
        collective.create_group(arg1=15, arg3=10)

    group_kwargs = {"arg3": 10, "arg1": 15}

    new_mock.assert_called_once_with(**group_kwargs)

    with mock.patch("lightning.fabric.plugins.collectives.single_device.SingleDeviceCollective.destroy_group"):
        collective.teardown()
