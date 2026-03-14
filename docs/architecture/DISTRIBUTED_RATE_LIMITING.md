# Distributed Rate Limiting with Token Bucket Algorithm

## Overview

PyAgent implements a distributed token bucket rate limiter with Redis backend to enforce per-agent quota limits across the fleet. This prevents runaway agents from exhausting shared resources like API quotas, compute budgets, or network bandwidth.

## Architecture

### Components

1. **DistributedTokenBucket**: Main rate limiter with Redis backend
2. **LocalTokenBucket**: In-memory fallback for when Redis is unavailable
3. **ResourceQuotaManager**: Facade that integrates rate limiting with existing quota enforcement
4. **CircuitBreaker**: Protects Redis from cascading failures

### Token Bucket Algorithm

The token bucket algorithm works as follows:

1. Each agent has a bucket with a maximum capacity of tokens
2. Tokens are consumed when performing operations (API calls, compute tasks, etc.)
3. Tokens refill at a constant rate over time
4. Operations are rejected when insufficient tokens are available

## Configuration

Set these environment variables to enable distributed rate limiting:

```bash
# Required: Redis connection URL
export REDIS_URL=redis://localhost:6379

# Optional: Token bucket size (default: 1000)
export TOKEN_BUCKET_SIZE=1000

# Optional: Refill rate in tokens/second (default: 10.0)
export TOKEN_REFILL_RATE=10.0
```

## Usage

### Basic Usage

```python
from src.core.base.logic.managers.resource_quota_manager import ResourceQuotaManager

# Initialize manager (reads config from environment)
manager = ResourceQuotaManager()

# Check and consume tokens before expensive operation
if await manager.check_and_consume("agent-123", tokens=10):
    # Proceed with operation
    result = await expensive_api_call()
else:
    # Quota exceeded, reject request
    raise ResourceExhaustedError("Rate limit exceeded")

# Cleanup when done
await manager.cleanup()
```

### Direct Token Bucket Usage

```python
from src.core.base.logic.managers.resource_quota_manager import DistributedTokenBucket

# Create token bucket with custom configuration
bucket = DistributedTokenBucket(
    redis_url="redis://localhost:6379",
    capacity=1000,
    refill_rate=10.0,
)

# Acquire tokens
if await bucket.acquire("agent-123", tokens=50):
    print("Tokens acquired successfully")
else:
    print("Insufficient tokens available")

# Check available tokens
available = await bucket.get_available_tokens("agent-123")
print(f"Available tokens: {available}")

# Reset bucket (useful for testing)
await bucket.reset_bucket("agent-123")

# Cleanup
await bucket.close()
```

## Graceful Degradation

The system gracefully degrades when Redis is unavailable:

1. **Initial Fallback**: If Redis URL is not configured, uses local in-memory bucket
2. **Connection Failure**: If Redis connection fails, falls back to local bucket
3. **Circuit Breaker**: After repeated failures, circuit breaker opens and requests use local bucket
4. **Recovery**: When Redis becomes available, circuit breaker automatically recovers

### Local Fallback Behavior

When using local fallback:
- All agents share the same token bucket (limitation of in-memory implementation)
- No fleet-wide enforcement (only local rate limiting)
- Suitable for single-node deployments or development environments

## Redis Implementation Details

### Atomic Operations

To prevent race conditions with concurrent access, the implementation uses Lua scripts executed atomically in Redis:

```lua
-- Token acquisition script
local tokens = get_current_tokens()
local elapsed = now - last_refill
tokens = min(capacity, tokens + elapsed * refill_rate)

if tokens >= requested then
    tokens = tokens - requested
    update_state(tokens, now)
    return 1  -- Success
else
    update_state(tokens, now)
    return 0  -- Insufficient tokens
end
```

### Key Schema

Redis keys follow this pattern:
```
quota:{agent_id}:tokens
```

Each key stores a hash with:
- `tokens`: Current token count (float)
- `last_refill`: Timestamp of last refill (float)

Keys expire after 1 hour of inactivity to prevent unbounded memory growth.

## Circuit Breaker Integration

The circuit breaker protects Redis from cascading failures:

- **Failure Threshold**: Opens after 3 consecutive failures
- **Recovery Timeout**: Attempts recovery after 30 seconds
- **Half-Open State**: Tests with limited requests before fully closing
- **Fail-Open**: When circuit is open, falls back to local bucket (allows operations to continue)

## Testing

### Unit Tests

Run local fallback tests (no Redis required):
```bash
pytest tests/unit/test_distributed_token_bucket.py -v
```

### Integration Tests

Run Redis integration tests (requires Redis):
```bash
# Start Redis
docker run -d -p 6379:6379 redis:latest

# Run tests
export REDIS_URL=redis://localhost:6379
pytest tests/unit/test_resource_quota_manager_redis.py -v
```

## Performance Considerations

### Redis Performance
- Each token acquisition requires 1 round-trip to Redis
- Lua script execution is atomic and very fast (~microseconds)
- Connection pooling reduces overhead of network connections

### Scaling
- Supports thousands of agents with minimal Redis load
- Redis can handle 100K+ operations/second on modest hardware
- For higher scale, consider Redis Cluster for horizontal scaling

### Monitoring
- Track circuit breaker stats to detect Redis issues
- Monitor Redis memory usage and connection pool
- Alert on frequent circuit breaker openings

## Security Considerations

- **Redis Authentication**: Always use Redis AUTH in production
- **Network Security**: Run Redis in private network, use TLS for encryption
- **Key Expiration**: Automatic cleanup prevents memory exhaustion
- **Input Validation**: Agent IDs are validated to prevent injection attacks

## Migration Guide

### Enabling Distributed Rate Limiting

1. Deploy Redis instance (or use existing Redis)
2. Set `REDIS_URL` environment variable
3. Configure `TOKEN_BUCKET_SIZE` and `TOKEN_REFILL_RATE` as needed
4. Restart PyAgent services
5. Monitor circuit breaker stats to verify Redis connectivity

### Disabling Distributed Rate Limiting

1. Remove `REDIS_URL` environment variable
2. Restart PyAgent services
3. System automatically falls back to local rate limiting

## Troubleshooting

### Circuit Breaker Frequently Opening
- Check Redis connectivity and health
- Verify Redis is not overloaded (check CPU/memory)
- Review Redis logs for errors
- Consider increasing recovery timeout

### Tokens Not Refilling
- Verify `TOKEN_REFILL_RATE` is set correctly
- Check for clock skew between nodes
- Review Redis key expiration settings

### Inconsistent Rate Limiting
- Ensure all nodes use same Redis instance
- Check for network partitions
- Verify `TOKEN_BUCKET_SIZE` and `TOKEN_REFILL_RATE` are consistent across fleet

## References

- Token Bucket Algorithm: https://en.wikipedia.org/wiki/Token_bucket
- Redis Lua Scripting: https://redis.io/docs/manual/programmability/eval-intro/
- Circuit Breaker Pattern: https://martinfowler.com/bliki/CircuitBreaker.html
