# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\test\clean_azure_test_data.py
import os
import sys

# We have to append user's current path to sys path so the modules can be resolved
# Otherwise we will got "no module named feathr" error
sys.path.append(os.path.abspath(os.getcwd()))

from click.testing import CliRunner
from feathr import FeathrClient
from feathrcli.cli import init


def clean_data():
    """
    Remove the test data(feature table: nycTaxiDemoFeature) in Azure.
    """
    client = FeathrClient()
    table_name = "nycTaxiDemoFeature"
    client._clean_test_data(table_name)
    print("Redis table cleaned: " + table_name)


runner = CliRunner()
with runner.isolated_filesystem():
    runner.invoke(init, [])
    # Need to be in the workspace so it won't complain
    os.chdir("feathr_user_workspace")
    clean_data()
