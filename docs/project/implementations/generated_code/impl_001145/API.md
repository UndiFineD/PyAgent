# API Reference

## component_1145.module

### ComponentState
State dataclass with:
- component_id
- status  
- data dict

### Component
Main class with execute() method.

## component_1145.api

### Async
- get_status(cid)
- update_config(cid, **kw)

### Sync
- sync_status(cid)
