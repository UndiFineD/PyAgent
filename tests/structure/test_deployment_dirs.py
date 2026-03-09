
import os


def test_deployment_tree_absent():
    # initially should fail because the directory doesn't exist
    assert os.path.isdir("Deployment")
