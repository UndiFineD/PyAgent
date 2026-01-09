# Description: `FederatedKnowledgeOrchestrator.py`

## Module purpose

FederatedKnowledgeOrchestrator for PyAgent.
Synchronizes learned insights ('Lessons Learned') between distributed fleet nodes.
Uses InterFleetBridgeOrchestrator to transmit knowledge without raw data leakage.

## Location
- Path: `src\classes\orchestration\FederatedKnowledgeOrchestrator.py`

## Public surface
- Classes: FederatedKnowledgeOrchestrator
- Functions: (none)

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `logging`, `typing`, `src.classes.orchestration.InterFleetBridgeOrchestrator`, `src.classes.context.KnowledgeAgent`

## Metadata

- SHA256(source): `4d77a46516295088`
- Last updated: `2026-01-08 22:53:25`
- File: `src\classes\orchestration\FederatedKnowledgeOrchestrator.py`