# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Multimodal Subsystem Design

The `src/multimodal` package will manage inputs and outputs that span text,
images, audio, and other media. Legacy code demonstrates an early agent
(`MultiModalContextAgent`) that processed screenshots and UI elements.

## Legacy Overview

> Agent specializing in visual context, UI analysis, and multimodal reasoning.
> Used for interpreting screenshots, diagrams, and vision-based UI testing.

The old implementation relied on `PIL`, `easyocr`, `pytesseract`, and
`pyautogui`; its methods included `analyze_screenshot`, `extract_text_from_image`,
and GUI recording/replay.

## Architectural Targets

- **Unified data model** (`MultiModalData`, `MultiModalInputs`) capturing raw
  content, embeddings, and metadata.
- **Processing pipeline** that converts raw media into embeddings or structural
  representations suitable for LLM ingestion.
- **Pluggable processors** for each modality (vision, audio, tts, formula
  parsing).
- **Async task queue** to handle expensive operations (image analysis,
  transcription) without blocking the main agent loop.

## Brainstorm Ideas

- Format negotiation and grammar‑constrained structured outputs (see
  Phase 26 notes in `comparison_vllm-old.md`).
- Multi‑stage pipelines: pre-processing, inference, post‑processing.
- Real‑time streaming support for audio/video inputs.
- Caching and deduplication of processed media.
- Integration with UI automation for screenshotting and interaction capture.

*Text reused from `src-old/classes/specialized/MultiModalContextAgent.py` and
todo list entry on multimodal integration.*