# Splice: src/observability/stats/histogram.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- HistogramBucket
- Histogram
- ExponentialHistogram
- LatencyHistogram
- SizeHistogram

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
