# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\main.py
from contextlib import asynccontextmanager
from pathlib import Path

from app import __version__
from app.api import health, models, predict, video
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import (
    APIKeyMiddleware,
    RequestLoggingMiddleware,
    setup_cors,
)
from app.core.registry import ModelRegistry
from app.tasks.inference import InferenceExecutor
from app.utils.update_checker import check_for_updates_async
from fastapi import FastAPI
from loguru import logger

settings, _ = get_settings()
setup_logging(settings.logging)

loader = None
inference_executor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Args:
        app: FastAPI application instance.
    """
    global loader, inference_executor

    logger.info("Starting X-AnyLabeling Server...")

    import os

    _, actual_server_config = get_settings()
    logger.info(f"Configuration loaded from {actual_server_config}")

    config_dir = Path(__file__).parent.parent / "configs"
    models_config_path = os.getenv("XANYLABELING_MODELS_CONFIG")
    if models_config_path:
        models_config_path = Path(models_config_path)
        logger.info(f"Models config loaded from {models_config_path}")
    else:
        models_config_path = None
        logger.info(f"Models config loaded from {config_dir / 'models.yaml'}")

    loader = ModelRegistry(config_dir, models_config_path=models_config_path)

    try:
        loader.load_all_models()
    except Exception as e:
        logger.error(f"Error during model loading: {e}")
        if len(loader.models) == 0:
            logger.warning("No models loaded, but continuing server startup")

    inference_executor = InferenceExecutor(
        loader=loader,
        max_workers=settings.concurrency.max_workers,
        max_queue_size=settings.concurrency.max_queue_size,
    )

    check_for_updates_async()

    yield

    logger.info("Shutting down server...")
    inference_executor.shutdown()
    loader.unload_all_models()
    logger.info("Server stopped")


app = FastAPI(
    title="X-AnyLabeling Server",
    description="AI Model Inference Service for X-AnyLabeling",
    version=str(__version__),
    lifespan=lifespan,
)

setup_cors(app, settings.security.cors_origins)

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    APIKeyMiddleware,
    enabled=settings.security.api_key_enabled,
    api_key=settings.security.api_key,
    header_name=settings.security.api_key_header,
)

app.include_router(health.router, tags=["Health"])
app.include_router(models.router, tags=["Models"])
app.include_router(predict.router, tags=["Prediction"])
app.include_router(video.router, tags=["Video"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.workers,
        reload=False,
    )
