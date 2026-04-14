# API Reference

## component_1252.module

### ComponentState
State dataclass with:
- component_id
- status  
- data dict

### Component
Main class with execute() method.

## component_1252.api

### Async
- get_status(cid)
- update_config(cid, **kw)

### Sync
- sync_status(cid)
