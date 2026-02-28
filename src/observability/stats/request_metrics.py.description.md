# Description: src/observability/stats/request_metrics.py

Module overview:
- Implements `RequestMetrics` dataclass and `RequestState` enum used to track detailed timing and state transitions for requests.
- Provides methods to mark lifecycle events (queued, scheduled, processing, first token, completed, failed) and computed timing properties (ms).

Primary types:
- `RequestState` (Enum)
- `RequestMetrics` (dataclass)

Behavioral notes:
- Designed for high-resolution latency analysis; includes convenience methods for marking events and computed properties for different timing buckets.
