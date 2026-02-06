# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\api\video.py
import base64
import json

import cv2
import numpy as np
from app.schemas.request import (
    VideoInitRequest,
    VideoPromptRequest,
    VideoPropagateRequest,
)
from app.schemas.response import (
    ErrorDetail,
    ErrorResponse,
    SuccessResponse,
)
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from loguru import logger

router = APIRouter()


@router.post("/v1/video/init")
async def init_video_session(request: VideoInitRequest):
    """Initialize video session with frame sequence.

    Args:
        request: Request containing model, frames, and start_frame_index.

    Returns:
        Success response with session_id or error response.
    """
    from app.main import loader

    model_id = request.model
    frames_data = request.frames
    start_frame_index = request.start_frame_index

    if not model_id:
        return ErrorResponse(
            error=ErrorDetail(code="MISSING_MODEL", message="Model ID is required")
        )

    if not frames_data:
        return ErrorResponse(
            error=ErrorDetail(code="MISSING_FRAMES", message="Frames are required")
        )

    try:
        model = loader.get_model(model_id)
    except ValueError as e:
        return ErrorResponse(error=ErrorDetail(code="MODEL_NOT_FOUND", message=str(e)))

    if not hasattr(model, "init_session"):
        return ErrorResponse(
            error=ErrorDetail(
                code="INVALID_MODEL",
                message="Model does not support video operations",
            )
        )

    try:
        frames = []
        for frame_data in frames_data:
            if "," in frame_data:
                frame_data = frame_data.split(",")[1]
            image_bytes = base64.b64decode(frame_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None:
                return ErrorResponse(
                    error=ErrorDetail(
                        code="INVALID_FRAME",
                        message=f"Failed to decode frame at index {len(frames)}",
                    )
                )
            frames.append(frame)

        result = model.init_session(frames, start_frame_index)

        if "error" in result:
            return ErrorResponse(
                error=ErrorDetail(code="INIT_ERROR", message=result["error"])
            )

        return SuccessResponse(data=result)

    except Exception as e:
        logger.error(f"Video session initialization error: {e}")
        return ErrorResponse(
            error=ErrorDetail(
                code="INIT_ERROR",
                message=f"Failed to initialize session: {str(e)}",
            )
        )


@router.post("/v1/video/prompt")
async def prompt_video_frame(request: VideoPromptRequest):
    """Add text or point prompt to a video frame.

    Args:
        request: Request containing session_id, text_prompt or points, frame_index, and params.

    Returns:
        Success response with masks or error response.
    """
    from app.main import loader

    session_id = request.session_id
    model_id = request.model
    text_prompt = request.text_prompt
    points = request.points
    point_labels = request.point_labels
    obj_id = request.obj_id
    frame_index = request.frame_index
    params = request.params

    if not session_id:
        return ErrorResponse(
            error=ErrorDetail(code="MISSING_SESSION", message="Session ID is required")
        )

    if not text_prompt and not points:
        return ErrorResponse(
            error=ErrorDetail(
                code="MISSING_PROMPT",
                message="Text prompt or points are required",
            )
        )

    try:
        model = loader.get_model(model_id)
    except ValueError as e:
        return ErrorResponse(error=ErrorDetail(code="MODEL_NOT_FOUND", message=str(e)))

    if not hasattr(model, "add_prompt"):
        return ErrorResponse(
            error=ErrorDetail(
                code="INVALID_MODEL",
                message="Model does not support video operations",
            )
        )

    try:
        if text_prompt:
            result = model.add_prompt(session_id, text_prompt, frame_index, params)
        else:
            result = model.add_point_prompt(
                session_id, points, point_labels, obj_id, frame_index, params
            )

        if "error" in result:
            return ErrorResponse(
                error=ErrorDetail(code="PROMPT_ERROR", message=result["error"])
            )

        return SuccessResponse(data=result)

    except Exception as e:
        logger.error(f"Video prompt error: {e}")
        return ErrorResponse(
            error=ErrorDetail(
                code="PROMPT_ERROR",
                message=f"Failed to process prompt: {str(e)}",
            )
        )


@router.post("/v1/video/propagate")
async def propagate_video(request: VideoPropagateRequest):
    """Start video propagation task.

    Args:
        request: Request containing session_id and optional frame range.

    Returns:
        Success response with task_id or error response.
    """
    from app.main import loader

    session_id = request.session_id
    model_id = request.model

    logger.info(
        f"Received propagate request: session_id={session_id}, model={model_id}"
    )

    try:
        model = loader.get_model(model_id)
    except ValueError as e:
        return ErrorResponse(error=ErrorDetail(code="MODEL_NOT_FOUND", message=str(e)))

    if not hasattr(model, "start_propagation"):
        return ErrorResponse(
            error=ErrorDetail(
                code="INVALID_MODEL",
                message="Model does not support video operations",
            )
        )

    try:
        result = model.start_propagation(
            session_id, request.start_frame, request.end_frame
        )

        if "error" in result:
            return ErrorResponse(
                error=ErrorDetail(code="PROPAGATION_ERROR", message=result["error"])
            )

        return SuccessResponse(
            data={
                "task_id": result["task_id"],
                "status": result.get("status", "processing"),
                "message": "Propagation started",
            }
        )

    except Exception as e:
        logger.error(f"Video propagation error: {e}")
        return ErrorResponse(
            error=ErrorDetail(
                code="PROPAGATION_ERROR",
                message=f"Failed to start propagation: {str(e)}",
            )
        )


@router.post("/v1/video/propagate/stream")
async def propagate_video_stream(request: VideoPropagateRequest):
    """Start video propagation with streaming response (SSE).

    Args:
        request: Request containing session_id and optional frame range.

    Returns:
        StreamingResponse with SSE events for progress and results.
    """
    import asyncio
    import queue
    import threading

    from app.main import loader

    session_id = request.session_id
    model_id = request.model

    try:
        model = loader.get_model(model_id)
    except ValueError as e:
        return ErrorResponse(error=ErrorDetail(code="MODEL_NOT_FOUND", message=str(e)))

    if not hasattr(model, "propagate_stream"):
        return ErrorResponse(
            error=ErrorDetail(
                code="INVALID_MODEL",
                message="Model does not support streaming propagation",
            )
        )

    event_queue = queue.Queue()
    propagation_done = threading.Event()
    stop_signal = threading.Event()

    def run_propagation():
        try:
            for event in model.propagate_stream(
                session_id, request.start_frame, request.end_frame
            ):
                if stop_signal.is_set():
                    logger.info("Propagation stopped by client disconnect")
                    break
                event_queue.put(event)
        except GeneratorExit:
            logger.info("Propagation generator closed")
        except Exception as e:
            logger.error(f"Stream propagation error: {e}")
            event_queue.put({"type": "error", "message": str(e)})
        finally:
            propagation_done.set()

    async def async_event_generator():
        thread = threading.Thread(target=run_propagation, daemon=True)
        thread.start()

        loop = asyncio.get_event_loop()
        try:
            while not propagation_done.is_set() or not event_queue.empty():
                try:
                    event = await asyncio.wait_for(
                        loop.run_in_executor(
                            None, lambda: event_queue.get(timeout=0.1)
                        ),
                        timeout=0.2,
                    )
                    yield f"data: {json.dumps(event)}\n\n"
                except (asyncio.TimeoutError, queue.Empty):
                    continue
        except GeneratorExit:
            logger.info("Client disconnected, stopping propagation")
            stop_signal.set()
        finally:
            stop_signal.set()

    return StreamingResponse(
        async_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Content-Type": "text/event-stream; charset=utf-8",
        },
    )


@router.get("/v1/video/status/{task_id}")
async def get_propagation_status(task_id: str):
    """Get propagation task status.

    Args:
        task_id: Task identifier.

    Returns:
        Success response with task status and progress.
    """
    from app.main import loader

    for model_instance in loader.models.values():
        if hasattr(model_instance, "get_task_status"):
            result = model_instance.get_task_status(task_id)
            if "error" not in result:
                return SuccessResponse(data=result)

    return ErrorResponse(
        error=ErrorDetail(code="TASK_NOT_FOUND", message=f"Task {task_id} not found")
    )


@router.post("/v1/video/cancel/{task_id}")
async def cancel_propagation(task_id: str):
    """Cancel propagation task.

    Args:
        task_id: Task identifier.

    Returns:
        Success response or error response.
    """
    from app.main import loader

    for model_instance in loader.models.values():
        if hasattr(model_instance, "cancel_task"):
            result = model_instance.cancel_task(task_id)
            if "error" not in result:
                return SuccessResponse(data=result)

    return ErrorResponse(
        error=ErrorDetail(code="TASK_NOT_FOUND", message=f"Task {task_id} not found")
    )


@router.post("/v1/video/cleanup/{session_id}")
async def cleanup_video_session(session_id: str, model: str):
    """Clean up and remove a video session.

    Args:
        session_id: Session identifier.
        model: Model identifier.

    Returns:
        Success response or error response.
    """
    from app.main import loader

    if not session_id:
        return ErrorResponse(
            error=ErrorDetail(code="MISSING_SESSION", message="Session ID is required")
        )

    try:
        model_instance = loader.get_model(model)
    except ValueError as e:
        return ErrorResponse(error=ErrorDetail(code="MODEL_NOT_FOUND", message=str(e)))

    if not hasattr(model_instance, "cleanup_session"):
        return ErrorResponse(
            error=ErrorDetail(
                code="INVALID_MODEL",
                message="Model does not support video operations",
            )
        )

    try:
        success = model_instance.cleanup_session(session_id)
        if success:
            return SuccessResponse(data={"message": f"Session {session_id} cleaned up"})
        return ErrorResponse(
            error=ErrorDetail(
                code="SESSION_NOT_FOUND",
                message=f"Session {session_id} not found",
            )
        )
    except Exception as e:
        logger.error(f"Session cleanup error: {e}")
        return ErrorResponse(
            error=ErrorDetail(
                code="CLEANUP_ERROR",
                message=f"Failed to cleanup session: {str(e)}",
            )
        )
