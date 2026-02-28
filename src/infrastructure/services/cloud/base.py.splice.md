# Splice: src/infrastructure/services/cloud/base.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- InferenceRequest
- InferenceResponse
- CloudProviderBase
- CloudProviderError
- RateLimitError
- AuthenticationError

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
