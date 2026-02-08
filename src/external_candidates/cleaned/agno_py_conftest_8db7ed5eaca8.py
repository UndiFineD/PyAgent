# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\tests.py\unit.py\vectordb.py\conftest_8db7ed5eaca8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\unit\vectordb\conftest.py

from typing import Any, Dict, List

from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session")
def mock_embedder():
    """Create a mock embedder with appropriate return values."""

    mock = MagicMock()

    # Mock dimensions property

    mock.dimensions = 1024

    # Create a fixed embedding vector of the correct size

    mock_embedding: List[float] = [0.1] * 1024

    # Mock the get_embedding method

    mock.get_embedding.return_value = mock_embedding

    # Mock the get_embedding_and_usage method

    mock_usage: Dict[str, Any] = {"prompt_tokens": 10, "total_tokens": 10}

    mock.get_embedding_and_usage.return_value = (mock_embedding, mock_usage)

    return mock
