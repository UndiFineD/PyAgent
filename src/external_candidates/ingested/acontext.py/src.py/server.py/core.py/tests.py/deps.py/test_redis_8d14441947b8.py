# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\tests\deps\test_redis.py
import pytest
from acontext_core.infra.redis import RedisClient


@pytest.mark.asyncio
async def test_redis_basic_operations():
    """Test basic Redis set/get/delete operations."""
    # Create a fresh client instance for this test
    client_instance = RedisClient()
    async with client_instance.get_client_context() as client:
        test_key = "test:basic"
        test_value = "test_value"

        # Set a value
        await client.set(test_key, test_value)

        # Get the value
        retrieved_value = await client.get(test_key)
        assert retrieved_value == test_value

        # Delete the key
        deleted = await client.delete(test_key)
        assert deleted == 1

        # Verify key is deleted
        exists = await client.exists(test_key)
        assert exists == 0

    # Clean up
    await client_instance.close()


@pytest.mark.asyncio
async def test_redis_connection():
    """Test Redis connection and ping."""
    # Create a fresh client instance for this test
    client_instance = RedisClient()
    async with client_instance.get_client_context() as client:
        response = await client.ping()
        assert response is True, "Redis ping should return True"

    # Clean up
    await client_instance.close()
