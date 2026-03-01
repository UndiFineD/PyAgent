# Improvements: src/observability/structured_logger.py

Potential improvements:
- Add unit tests that verify masking, fallback to Python path, and gzip rotation behavior using temporary directories.
- Make the log file path injectable for tests to avoid writing into `data/logs` during CI.
- Reduce reliance on broad except blocks; handle expected exceptions explicitly and preserve tracebacks for debugging.
- Consider exposing a pluggable serializer to allow alternate output formats (NDJSON, protobuf) for integration.
- Add asyncio-compatible non-blocking write path or background worker to avoid blocking the calling thread during file I/O.
- Add configuration options for maximum file size, compression strategy, and retention policy.
- Add more granular unit tests for `mask_sensitive` with a varied set of patterns.
- Use structured type annotations and dataclasses for configuration parameters.
