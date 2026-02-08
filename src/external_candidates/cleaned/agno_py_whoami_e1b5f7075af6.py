# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\infra.py\agno_docker.py\agno.py\docker.py\app.py\whoami.py\whoami_e1b5f7075af6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\infra\agno_docker\agno\docker\app\whoami\whoami.py

from agno.docker.app.base import ContainerContext, DockerApp  # noqa: F401

class Whoami(DockerApp):

    # -*- App Name

    name: str = "whoami"

    # -*- Image Configuration

    image_name: str = "traefik/whoami"

    image_tag: str = "v1.10"

    # -*- App Ports

    # Open a container port if open_port=True

    open_port: bool = True

    port_number: int = 80

