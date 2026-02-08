# Extracted from: C:\DEV\PyAgent\.external\big-3-super-agent\apps\content-gen\backend\src\content_gen_backend\__main__.py
"""Run the development server."""

import uvicorn


def main():
    """Start the development server with reload enabled."""
    uvicorn.run(
        "content_gen_backend.main:app",
        host="0.0.0.0",
        port=4444,
        reload=True,
    )


if __name__ == "__main__":
    main()
