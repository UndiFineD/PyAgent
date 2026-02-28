# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_docker\agno\docker\app\postgres\pgvector.py
from agno.docker.app.postgres.postgres import PostgresDb


class PgVectorDb(PostgresDb):
    # -*- App Name
    name: str = "pgvector"

    # -*- Image Configuration
    image_name: str = "agnohq/pgvector"
    image_tag: str = "16"
