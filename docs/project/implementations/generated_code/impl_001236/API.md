# API Reference

## component_1236.module

### ComponentState
State dataclass with:
- component_id
- status  
- data dict

### Component
Main class with execute() method.

## component_1236.api

### Async
- get_status(cid)
- update_config(cid, **kw)

### Sync
- sync_status(cid)
