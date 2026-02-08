# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\big_3_super_agent.py\apps.py\content_gen.py\backend.py\src.py\content_gen_backend.py\main_b6dbdb061259.py
# NOTE: extracted with static-only rules; review before use

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
