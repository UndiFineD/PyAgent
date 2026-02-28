# Description: src/observability/stats/alerting.py

Module overview:
- Provides `ThresholdAlertManager` for threshold-based alert creation and `RetentionEnforcer` for enforcing retention policies on metric data.
- Uses optional `rust_core` acceleration for policy matching.

Primary classes:
- `ThresholdAlertManager`: manage thresholds and check metric breaches producing `Alert` objects.
- `RetentionEnforcer`: apply retention policies to stored metric data and remove expired entries.

Behavioral notes:
- `ThresholdAlertManager.check` returns triggered `Alert` objects and appends them to an internal list.
- `RetentionEnforcer` supports both Rust-accelerated pattern matching and a Python fallback.
