# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\test\init\test_env_variables.py
from init.env_variables import BASE_PATH, SOCKET_URL


class TestEnvariables:
    # Assert that the constants are not null
    def test_non_null_constants(self):
        assert len(SOCKET_URL) > 0
        assert len(BASE_PATH) > 0
