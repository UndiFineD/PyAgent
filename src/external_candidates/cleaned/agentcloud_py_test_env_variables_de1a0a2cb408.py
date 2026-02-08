# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\test.py\init.py\test_env_variables_de1a0a2cb408.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\test\init\test_env_variables.py

from init.env_variables import BASE_PATH, SOCKET_URL


class TestEnvariables:
    # Assert that the constants are not null

    def test_non_null_constants(self):

        assert len(SOCKET_URL) > 0

        assert len(BASE_PATH) > 0
