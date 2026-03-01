# Description: src/observability/stats/api.py

Module overview:
- Defines `APIEndpoint` dataclass and `StatsAPIServer` for a minimal stats API server interface.

Behavioral notes:
- Provides methods to register endpoints, handle basic requests, and generate simple OpenAPI-like docs.
- `handle_request` uses simplistic path matching and a placeholder for `stats_agent.calculate_stats()`.
