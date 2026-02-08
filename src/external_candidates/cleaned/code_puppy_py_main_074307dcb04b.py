# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\code_puppy.py\code_puppy.py\api.py\main_074307dcb04b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\code_puppy\code_puppy\api\main.py

"""Entry point for running the FastAPI server."""

import uvicorn

from code_puppy.api.app import create_app

app = create_app()


def main(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Run the FastAPI server.

    Args:

        host: The host address to bind to. Defaults to localhost.

        port: The port number to listen on. Defaults to 8765.

    """

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
