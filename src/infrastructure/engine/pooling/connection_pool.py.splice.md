# Splice: src/infrastructure/engine/pooling/connection_pool.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ConnectionState
- Closeable
- Pingable
- PoolStats
- PooledConnection
- ConnectionPool
- AsyncConnectionPool
- PooledConnectionManager
- MultiHostPool

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
