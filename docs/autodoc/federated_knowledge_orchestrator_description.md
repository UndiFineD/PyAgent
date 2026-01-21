# Description: `FederatedKnowledgeOrchestrator.py`

## Module purpose

FederatedKnowledgeOrchestrator for PyAgent.
Synchronizes learned insights ('Lessons Learned') between distributed fleet nodes.
Uses InterFleetBridgeOrchestrator to transmit knowledge without raw data leakage.

## Location
- Path: `src\infrastructure\orchestration\FederatedKnowledgeOrchestrator.py`

## Public surface
- Classes: FederatedKnowledgeOrchestrator
- Functions: (none)

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `__future__`, `logging`, `typing`, `src.infrastructure.orchestration.InterFleetBridgeOrchestrator`, `src.logic.agents.cognitive.KnowledgeAgent`

## Metadata

- SHA256(source): `3c7b1a13627c6b01`
- Last updated: `2026-01-11 10:15:44`
- File: `src\infrastructure\orchestration\FederatedKnowledgeOrchestrator.py`