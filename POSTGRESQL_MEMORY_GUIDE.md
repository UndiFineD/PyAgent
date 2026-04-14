# PostgreSQL Memory System - Usage Guide

## Quick Start

```python
from memory_system import UnifiedMemorySystem

# Initialize
memory = UnifiedMemorySystem()
memory.initialize()

# Use key-value store
memory.kv.set("user:1:name", "Alice")
name = memory.kv.get("user:1:name")

# Use B-Tree for sorted data
memory.btree.insert(1, "item_1")
memory.btree.insert(2, "item_2")
results = memory.btree.range(1, 2)

# Use transactions for atomicity
with memory.transaction():
    memory.kv.set("key1", "val1")
    memory.kv.set("key2", "val2")
    # Auto-commit on success, rollback on exception
```

## Virtual Paths

### 1. KV Store (Key-Value)
Fast O(1) lookups with optional TTL

```python
# Set with TTL
memory.kv.set("session:abc123", data, ttl_seconds=3600)

# Get
value = memory.kv.get("session:abc123")

# Delete
memory.kv.delete("session:abc123")

# Scan with prefix
memory.kv.scan(prefix="user:")
```

### 2. B-Tree Index
Sorted range queries

```python
# Insert
memory.btree.insert(key=100, value="data")

# Range query
items = memory.btree.range(min_key=50, max_key=150)

# Full scan (sorted)
all_items = memory.btree.scan()

# Delete
memory.btree.delete(100)
```

### 3. Linked List
Ordered sequences and timelines

```python
# Append to list
memory.linked_list.append("event_1")
memory.linked_list.append("event_2")

# Pop from end
last = memory.linked_list.pop()

# Iterate
for item in memory.linked_list.iterate():
    print(item)

# Length
size = memory.linked_list.length()
```

### 4. Graph (DAG)
Dependency tracking

```python
# Add nodes
memory.graph.add_node("task_1")
memory.graph.add_node("task_2")

# Add edges
memory.graph.add_edge("task_1", "task_2")

# Get dependencies
deps = memory.graph.get_dependencies("task_2")  # ["task_1"]

# Topological sort
order = memory.graph.topological_sort()
```

### 5. Kanban Board
Workflow tracking

```python
# Add task
memory.kanban.add_task("BACKLOG", "feature_1")

# Move task
memory.kanban.move_task("feature_1", "IN_PROGRESS")

# Get tasks by status
backlog = memory.kanban.get_tasks("BACKLOG")
in_progress = memory.kanban.get_tasks("IN_PROGRESS")

# View full board
board = memory.kanban.get_board()
```

### 6. Lessons Learned
Pattern recurrence tracking

```python
# Record a lesson
memory.lessons.record(
    pattern="import_error",
    lesson="Use absolute imports",
    severity="high"
)

# Find similar patterns
similar = memory.lessons.find_similar("import_error")

# Track recurrence
memory.lessons.increase_recurrence(lesson_id=1)

# Get high recurrence lessons
critical = memory.lessons.get_high_recurrence(threshold=5)
```

### 7. Code Ledger
Implementation metrics

```python
# Log implementation
memory.code_ledger.log_impl(feature="auth_system", loc=250)

# Get metrics for feature
metrics = memory.code_ledger.get_metrics("auth_system")

# Total LOC
total = memory.code_ledger.total_loc()

# List all implementations
impls = memory.code_ledger.get_implementations()
```

## Transactions

### Context Manager (Recommended)

```python
# Auto-commit on success, auto-rollback on exception
with memory.transaction() as tx:
    memory.kv.set("key1", "value1")
    memory.btree.insert(10, "data")
    memory.kanban.add_task("BACKLOG", "task")
    # All succeed together or all fail together
```

### Manual Control

```python
tx = memory.new_transaction()
tx.begin_sync()

try:
    memory.kv.set("key", "value")
    memory.btree.insert(1, "item")
    tx.commit_sync()
except Exception as e:
    tx.rollback_sync()
    raise
```

### Savepoints

```python
with memory.transaction() as tx:
    memory.kv.set("key1", "value1")
    
    # Create savepoint
    sp1 = tx.create_savepoint("after_key1")
    
    memory.kv.set("key2", "value2")
    
    # Rollback to savepoint if needed
    if error_condition:
        tx.rollback_to_savepoint("after_key1")
    
    # Both savepoints commit together
```

## Configuration

File: `~/PyAgent/memory_config.json`

```json
{
  "backend": "postgresql",
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "hermes_memory",
    "user": "postgres",
    "password": "postgres"
  },
  "features": {
    "transactions": true,
    "savepoints": true,
    "acid_compliance": true
  }
}
```

## Monitoring

### Check Database
```bash
psql -U postgres -d hermes_memory -c "\dt"
```

### View KV Store
```bash
psql -U postgres -d hermes_memory -c "SELECT key, value FROM kv_store LIMIT 10;"
```

### Database Size
```bash
psql -U postgres -d hermes_memory -c "SELECT pg_size_pretty(pg_database_size('hermes_memory'));"
```

### Active Connections
```bash
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE datname='hermes_memory';"
```

## Backup & Restore

### Backup
```bash
pg_dump -U postgres -d hermes_memory > hermes_backup.sql

# Or compressed
pg_dump -U postgres -d hermes_memory | gzip > hermes_backup.sql.gz
```

### Restore
```bash
psql -U postgres -d hermes_memory < hermes_backup.sql

# Or from compressed
gunzip -c hermes_backup.sql.gz | psql -U postgres -d hermes_memory
```

### Scheduled Backups
```bash
# Add to crontab
0 2 * * * pg_dump -U postgres hermes_memory > ~/backups/hermes_$(date +\%Y\%m\%d).sql
```

## Performance Tips

1. **Use KV Store for Hot Reads**
   - O(1) lookup time
   - Perfect for caches and sessions

2. **Use B-Tree for Range Queries**
   - Sorted iteration
   - Efficient range scans

3. **Transaction Scope**
   - Keep transactions small
   - Minimize lock duration

4. **Connection Pooling**
   - Reuse connections
   - Reduce connection overhead

5. **Indexes**
   - Automatic on primary keys
   - Consider custom indexes for large datasets

## Troubleshooting

### Connection Issues
```bash
# Test connection
psql -U postgres -h localhost -d hermes_memory -c "SELECT 1;"

# Check server status
psql -U postgres -c "SELECT version();"
```

### Permission Denied
```bash
# Reset password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'new_password';"

# Update config
export POSTGRES_PASSWORD=new_password
```

### Database Doesn't Exist
```bash
# Create it
createdb -U postgres hermes_memory

# Reinitialize schema
python3 -c "from memory_system import UnifiedMemorySystem; m = UnifiedMemorySystem(); m.initialize()"
```

### Performance Degradation
```bash
# Run maintenance
psql -U postgres -d hermes_memory -c "VACUUM ANALYZE;"

# Check table sizes
psql -U postgres -d hermes_memory -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"
```

## Integration with Hermes

The PostgreSQL memory system is integrated with Hermes:

```bash
# Use in Hermes tools
hermes /tool memory_stats action=execute

# Use in Hermes skills
hermes /skill memory_system execute

# Access from Hermes agent
from memory_system import UnifiedMemorySystem
```

## API Reference

### UnifiedMemorySystem

```python
class UnifiedMemorySystem:
    def __init__(host, port, database, user, password)
    def initialize() -> bool
    def new_transaction() -> MemoryTransaction
    def transaction() -> ContextManager
    
    # Virtual paths
    kv: KVStore
    btree: BTreeIndex
    linked_list: LinkedList
    graph: Graph
    kanban: KanbanBoard
    lessons: LessonLearned
    code_ledger: CodeImplementationLedger
```

---

**Version**: 1.0.0  
**Backend**: PostgreSQL 12+  
**Status**: Production Ready
