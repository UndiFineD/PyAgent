# Prj0000035 Multimodal Subsystem

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Build the `src/multimodal` package that manages text, image, audio, and other
media inputs/outputs. The subsystem converts raw media into embeddings or
structured representations that LLMs can consume, using an async task queue
so expensive operations don't block the agent loop.

## Architecture

- **Unified data model** — `MultiModalData` capturing raw content, embeddings,
  and metadata across modalities.
- **Processing pipeline** — raw media → pre-process → inference → post-process.
- **Pluggable processors** — vision, audio, TTS, formula parsing; each
  registered via a processor registry.
- **Async task queue** — expensive operations (image analysis, transcription)
  dispatched off the critical path.

## Tasks

- [ ] Define `MultiModalData` and `MultiModalInputs` data models
- [ ] Implement processor base class `ModalityProcessor` ABC
- [ ] Implement vision processor (screenshot analysis, OCR, embeddings)
- [ ] Implement audio processor (transcription, TTS)
- [ ] Implement async task queue for processor dispatch (`asyncio.Queue`)
- [ ] Implement format negotiation and grammar-constrained structured outputs
- [ ] Add caching and deduplication layer for processed media
- [ ] Implement streaming support for audio/video inputs
- [ ] Integrate with UI automation for screenshot capture
- [ ] Write tests: `tests/test_multimodal.py`
- [ ] Document design in `docs/architecture/multimodal.md`

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Data models defined | T1 | NOT_STARTED |
| M2 | Processor base and vision | T2, T3 | NOT_STARTED |
| M3 | Audio and async queue | T4, T5 | NOT_STARTED |
| M4 | Format negotiation, cache, streaming | T6, T7, T8 | NOT_STARTED |
| M5 | UI integration, tests, docs | T9, T10, T11 | NOT_STARTED |
