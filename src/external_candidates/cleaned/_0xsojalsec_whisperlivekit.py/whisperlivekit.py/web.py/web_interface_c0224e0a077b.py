# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-WhisperLiveKit\whisperlivekit\web\web_interface.py
import importlib.resources as resources
import logging

logger = logging.getLogger(__name__)


def get_web_interface_html():
    """Loads the HTML for the web interface using importlib.resources."""
    try:
        with resources.files("whisperlivekit.web").joinpath("live_transcription.html").open("r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading web interface HTML: {e}")
        return "<html><body><h1>Error loading interface</h1></body></html>"


if __name__ == "__main__":
    import pathlib

    import uvicorn
    import whisperlivekit.web as webpkg
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from starlette.staticfiles import StaticFiles

    app = FastAPI()
    web_dir = pathlib.Path(webpkg.__file__).parent
    app.mount("/web", StaticFiles(directory=str(web_dir)), name="web")

    @app.get("/")
    async def get():
        return HTMLResponse(get_web_interface_html())

    uvicorn.run(app=app)
