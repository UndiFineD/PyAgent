# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\infra.py\agno_docker.py\agno.py\docker.py\app.py\postgres.py\pgvector_87d5866b8751.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_docker\agno\docker\app\postgres\pgvector.py

from agno.docker.app.postgres.postgres import PostgresDb


class PgVectorDb(PostgresDb):
    # -*- App Name

    name: str = "pgvector"

    # -*- Image Configuration

    image_name: str = "agnohq/pgvector"

    image_tag: str = "16"
