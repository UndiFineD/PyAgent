# API Reference

## component_1335.module

### ComponentState
State dataclass with:
- component_id
- status  
- data dict

### Component
Main class with execute() method.

## component_1335.api

### Async
- get_status(cid)
- update_config(cid, **kw)

### Sync
- sync_status(cid)
