# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\test.py\qdrantclient.py\test_qdrant_connection_dd7dc0b36655.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\test\qdrantClient\test_qdrant_connection.py

# test_qdrant_connection.py

import pytest

import qdrant.qdrant_connection as qdc


@pytest.mark.require_docker_compose_up
class TestQdrantConnection:
    def test_get_connection_success(self):
        # Test the successful creation of a Qdrant connection

        # Replace 'localhost' and 6333 with actual values if different

        client = qdc.get_connection(host="localhost", port=6333)

        assert client is not None

    def test_get_connection_invalid_host(self):
        # Test connection failure due to invalid host

        with pytest.raises(ValueError):
            qdc.get_connection(host="", port=6333)

    def test_get_connection_invalid_port(self):
        # Test connection failure due to invalid port

        with pytest.raises(ValueError):
            qdc.get_connection(host="localhost", port=0)
