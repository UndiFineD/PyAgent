# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\test\test_config_loading.py
import os

from click.testing import CliRunner
from feathr import FeathrClient
from feathrcli.cli import init


def test_configuration_loading():
    """
    Test the configuration can be overwritten by envs
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(init, [])

        assert result.exit_code == 0
        assert os.path.isdir("./feathr_user_workspace")

        client = FeathrClient(config_path="./feathr_user_workspace/feathr_config.yaml")

        # test the loading is correct even if we are not in that folder
        assert client._FEATHR_JOB_JAR_PATH is not None

        SPARK_RESULT_OUTPUT_PARTS = "4"

        # Use a less impactful config to test, as this config might be impactful for all the tests (since it's setting the envs)
        os.environ["SPARK_CONFIG__SPARK_RESULT_OUTPUT_PARTS"] = SPARK_RESULT_OUTPUT_PARTS

        # this should not be error out as we will just give users prompt, though the config is not really here
        client = FeathrClient(config_path="./feathr_user_workspace/feathr_config.yaml")
        assert client.output_num_parts == SPARK_RESULT_OUTPUT_PARTS
