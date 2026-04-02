# PostgreSQL 16 Setup — AutoMem Hybrid Search
## prj0000079 — automem-hybrid-search

---

## 1. Prerequisites

| Requirement | Version |
|-------------|---------|
| PostgreSQL | **16.x** |
| pgvector | **0.7+** |
| Apache AGE | **1.5+** |
| Python | 3.11+ |
| asyncpg | 0.29+ |

---

## 2. Installation

### 2a. Windows (`winget`)

```powershell
# Install PostgreSQL 16 (includes pgAdmin)
winget install PostgreSQL.PostgreSQL.16

# Verify
psql --version        # PostgreSQL 16.x
```

> **Note:** The PostgreSQL installer on Windows ships with **Stack Builder**. After
> installation completes, open Stack Builder and install **pgvector** from the
> *Database Drivers* category.

### 2b. macOS (Homebrew)

```bash
brew install postgresql@16 pgvector

# Start service
brew services start postgresql@16

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2c. Debian / Ubuntu (APT)

```bash
# Add official PGDG repo
sudo apt install -y curl ca-certificates lsb-release
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/postgresql.gpg
echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] \
  https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
  | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt install -y postgresql-16 postgresql-16-pgvector
```

### 2d. Docker (fastest for local dev)

```yaml
# docker-compose.yml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: pyagent
      POSTGRES_PASSWORD: pyagent
      POSTGRES_DB: automem
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d
```

> The `pgvector/pgvector:pg16` image includes pgvector pre-installed.

---

## 3. Apache AGE Installation

Apache AGE is **not** bundled with standard PostgreSQL packages.
Build from source (recommended) or use the PGDG binaries where available.

### Build from source (all platforms)

```bash
# Prerequisites
sudo apt install postgresql-server-dev-16 build-essential libreadline-dev zlib1g-dev flex bison

git clone https://github.com/apache/age.git
cd age
git checkout v1.5.0-rc0

make PG_CONFIG=$(which pg_config)
sudo make install PG_CONFIG=$(which pg_config)
```

### Windows

Use the pre-built DLLs from the AGE GitHub releases page:
<https://github.com/apache/age/releases>

Copy `age.dll` and `age.control` to the PostgreSQL extension directory:

```powershell
$pgShare = (pg_config --sharedir)
$pgLib   = (pg_config --pkglibdir)
Copy-Item age.dll         "$pgLib\"
Copy-Item age.control     "$pgShare\extension\"
Copy-Item age--*.sql      "$pgShare\extension\"
```

---

## 4. Create the Database

```sql
-- Connect as superuser (postgres)
psql -U postgres

CREATE DATABASE automem
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8';

CREATE USER pyagent WITH PASSWORD 'pyagent';
GRANT ALL PRIVILEGES ON DATABASE automem TO pyagent;

-- Required for AGE: superuser or explicit pg_read_server_files privilege
ALTER ROLE pyagent SUPERUSER;   -- for dev only; tighten in production
```

---

## 5. Install Extensions

Connect to the `automem` database:

```bash
psql -U postgres -d automem
```

```sql
-- Core extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- UUID generation
CREATE EXTENSION IF NOT EXISTS vector;         -- pgvector: HNSW / IVFFlat
CREATE EXTENSION IF NOT EXISTS ltree;          -- parent-child hierarchy
CREATE EXTENSION IF NOT EXISTS pg_trgm;        -- trigram similarity
CREATE EXTENSION IF NOT EXISTS btree_gin;      -- GIN on btree types
CREATE EXTENSION IF NOT EXISTS btree_gist;     -- GiST on btree types
CREATE EXTENSION IF NOT EXISTS age;            -- Apache AGE (graph)
CREATE EXTENSION IF NOT EXISTS pgcrypto;       -- UUID + crypto helpers

-- Verify
SELECT name, default_version, installed_version
FROM pg_available_extensions
WHERE name IN ('vector','age','ltree','pg_trgm','btree_gin','btree_gist');
```

Expected output:

```
   name    | default_version | installed_version
-----------+-----------------+-------------------
 age       | 1.5.0           | 1.5.0
 btree_gin | 1.3             | 1.3
 btree_gist| 1.7             | 1.7
 ltree     | 1.2             | 1.2
 pg_trgm   | 1.6             | 1.6
 vector    | 0.7.0           | 0.7.0
```

---

## 6. Apply the Schema

```bash
psql -U pyagent -d automem -f src/core/memory/schema.sql
```

Or from within psql:

```sql
\i src/core/memory/schema.sql
```

Verify tables and indexes:

```sql
\d memories          -- all columns
\di memories         -- all indexes (B-tree, HNSW, GIN, GiST, SP-GiST, BRIN, Hash)
```

---

## 7. `postgresql.conf` Tuning (recommended)

Edit `postgresql.conf` (find with `SHOW config_file;`):

```ini
# Memory
shared_buffers        = 512MB          # 25% of RAM
effective_cache_size  = 2GB            # 50-75% of RAM
work_mem              = 64MB           # per sort/hash operation
maintenance_work_mem  = 256MB          # for VACUUM, index builds

# HNSW / pgvector
max_parallel_workers_per_gather = 2

# Apache AGE
shared_preload_libraries = 'age'       # required to load AGE at startup

# Connections
max_connections = 100
```

Restart PostgreSQL after changes:

```bash
# Linux
sudo systemctl restart postgresql@16-main

# macOS
brew services restart postgresql@16

# Windows (PowerShell)
Restart-Service postgresql-x64-16
```

---

## 8. Python Dependencies

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

pip install asyncpg pgvector
```

Or add to `requirements.txt`:

```
asyncpg>=0.29.0
pgvector>=0.3.0
```

---

## 9. Verify the Stack

```python
# Quick smoke test — run from repo root
import asyncio, asyncpg

async def check():
    conn = await asyncpg.connect(
        "postgresql://pyagent:pyagent@localhost/automem"
    )
    # pgvector
    result = await conn.fetchval("SELECT '[1,2,3]'::vector(3)")
    print("pgvector OK:", result)
    # ltree
    path = await conn.fetchval("SELECT 'root.a.b'::ltree")
    print("ltree OK:", path)
    # age
    try:
        rows = await conn.fetch("SELECT * FROM ag_graph")
        print("AGE OK: graph table accessible", len(rows), "graphs")
    except Exception as e:
        print("AGE check:", e)
    await conn.close()

asyncio.run(check())
```

---

## 10. Benchmark Quick-Start

```bash
# Seed 1 000 random rows and benchmark all index methods
python -m src.core.memory.BenchmarkRunner \
    postgresql://pyagent:pyagent@localhost/automem \
    100 500 1000
```

Output is JSON suitable for piping into the web benchmark dashboard.

---

## 11. Index Reference

| Index | Type | Column(s) | Purpose |
|-------|------|-----------|---------|
| `idx_mem_agent_id` | B-tree | `agent_id` | Agent scoping |
| `idx_mem_created_at` | B-tree | `created_at DESC` | Recency sort |
| `idx_mem_importance` | B-tree | `importance DESC` | Importance sort |
| `idx_mem_access` | B-tree | `access_count DESC` | Frecency |
| `idx_mem_agent_recent` | B-tree composite | `(agent_id, created_at DESC)` | Hot-path: agent+recency |
| `idx_mem_hnsw` | HNSW (pgvector) | `embedding vector_cosine_ops` | ANN vector search |
| `idx_mem_tsv` | GIN | `tsv` | Full-text search |
| `idx_mem_keywords` | GIN | `keywords TEXT[]` | Keyword array match |
| `idx_mem_tags` | GIN | `tags TEXT[]` | Tag filter |
| `idx_mem_metadata` | GIN | `metadata JSONB` | Metadata filter |
| `idx_mem_path` | GiST | `path LTREE` | Hierarchy traversal |
| `idx_mem_content_trgm` | GiST trgm | `content` | LIKE / similarity |
| `idx_mem_path_spgist` | SP-GiST | `path LTREE` | Balanced hierarchy alt. |
| `idx_mem_brin_created` | BRIN | `created_at` | Range scan (large tables) |
| `idx_mem_hash_agent` | Hash | `agent_id` | Equality-only fast read |
| `idx_mem_hash_session` | Hash | `session_id` | Session lookup |
