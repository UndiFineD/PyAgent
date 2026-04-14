# API Reference

## component_1104.module

### ComponentState
State dataclass with:
- component_id
- status  
- data dict

### Component
Main class with execute() method.

## component_1104.api

### Async
- get_status(cid)
- update_config(cid, **kw)

### Sync
- sync_status(cid)
