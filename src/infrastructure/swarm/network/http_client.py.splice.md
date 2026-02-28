# Splice: src/infrastructure/swarm/network/http_client.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- HTTPClient
- AsyncHTTPClient
- RetryableHTTPClient

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
