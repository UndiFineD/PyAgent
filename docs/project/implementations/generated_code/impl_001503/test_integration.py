"""Integration tests for impl_001503.
"""
import pytest
from api import get_status, process_request


def test_api_status():
    """Test API status endpoint."""
    status = get_status()
    assert status["status"] == "ok"

def test_api_process():
    """Test API processing."""
    result = process_request({"input": "test"})
    assert "result" in result

@pytest.mark.integration
def test_full_workflow():
    """Test complete workflow."""
    status = get_status()
    assert status is not None
    result = process_request(status)
    assert result["status"] == "processed"
