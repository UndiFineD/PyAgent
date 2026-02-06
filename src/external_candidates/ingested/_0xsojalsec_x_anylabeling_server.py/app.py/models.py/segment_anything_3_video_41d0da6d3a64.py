# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\models\segment_anything_3_video.py
import os
import shutil
import sys
import tempfile
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import torch
from app.core.registry import register_model
from loguru import logger

from . import BaseModel


class _TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class _VideoSession:
    """Internal video session for SAM3."""

    def __init__(
        self,
        session_id: str,
        frames: List[np.ndarray],
        start_frame_index: int,
        predictor: Any,
    ):
        """Initialize video session.

        Args:
            session_id: Unique session identifier.
            frames: List of video frames as numpy arrays.
            start_frame_index: Starting frame index in original sequence.
            predictor: SAM3 video predictor instance.
        """
        self.session_id = session_id
        self.frames = frames
        self.start_frame_index = start_frame_index
        self.predictor = predictor
        self.text_prompt: Optional[str] = None
        self.is_point_prompt: bool = False
        self.last_prompt_frame: Optional[int] = None
        self.prompt_frame_outputs: Optional[Dict[str, Any]] = None
        self.prompt_frame_params: Optional[Dict[str, Any]] = None
        self.created_at = time.time()
        self.temp_dir: Optional[str] = None
        self._init_predictor_session()

    def _init_predictor_session(self):
        """Create temporary directory and initialize predictor session."""
        self.temp_dir = tempfile.mkdtemp(prefix="sam3_video_")
        frame_dir = os.path.join(self.temp_dir, "frames")
        os.makedirs(frame_dir, exist_ok=True)

        for i, frame in enumerate(self.frames):
            frame_path = os.path.join(frame_dir, f"{i:05d}.jpg")
            cv2.imwrite(frame_path, frame)

        self.predictor.handle_request(
            request=dict(
                type="start_session",
                resource_path=frame_dir,
                session_id=self.session_id,
            )
        )
        logger.info(
            f"Created video session {self.session_id} with {len(self.frames)} frames"
        )

    def cleanup(self):
        """Clean up session resources."""
        try:
            self.predictor.handle_request(
                request=dict(type="close_session", session_id=self.session_id)
            )
        except Exception as e:
            logger.warning(f"Error closing session {self.session_id}: {e}")

        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)


class _PropagationTask:
    """Internal propagation task for SAM3."""

    def __init__(
        self,
        task_id: str,
        session_id: str,
        start_frame: Optional[int] = None,
        end_frame: Optional[int] = None,
    ):
        """Initialize propagation task.

        Args:
            task_id: Unique task identifier.
            session_id: Video session identifier.
            start_frame: Optional start frame index.
            end_frame: Optional end frame index.
        """
        self.task_id = task_id
        self.session_id = session_id
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.status = _TaskStatus.PENDING
        self.progress = 0.0
        self.current_frame = 0
        self.total_frames = 0
        self.results: Dict[int, Any] = {}
        self.error: Optional[str] = None
        self.created_at = time.time()
        self.lock = threading.Lock()
        self._cancelled = False

    def cancel(self):
        """Cancel the task."""
        with self.lock:
            self._cancelled = True
            if self.status == _TaskStatus.PROCESSING:
                self.status = _TaskStatus.CANCELLED

    def is_cancelled(self) -> bool:
        """Check if task is cancelled."""
        with self.lock:
            return self._cancelled


@register_model("segment_anything_3_video")
class SegmentAnything3Video(BaseModel):
    """Segment Anything Model 3 for video segmentation with text prompts."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize SAM3 video model.

        Args:
            config: Model configuration dictionary.
        """
        super().__init__(config)
        self.predictor = None
        self._sessions: Dict[str, _VideoSession] = {}
        self._tasks: Dict[str, _PropagationTask] = {}
        self._sessions_lock = threading.Lock()
        self._tasks_lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._max_sessions = 10
        self._session_timeout = 1800

    def load(self):
        """Load SAM3 video model and initialize components."""
        sam3_parent_dir = os.path.join(os.path.dirname(__file__))
        if sam3_parent_dir not in sys.path:
            sys.path.insert(0, sam3_parent_dir)

        from sam3.model_builder import build_sam3_video_predictor

        bpe_path = self.params.get("bpe_path")
        model_path = self.params.get("model_path")
        devices = self.params.get("devices", [0])

        if isinstance(devices, list) and devices:
            gpus_to_use = range(len(devices))
        elif isinstance(devices, int):
            gpus_to_use = range(devices)
        else:
            gpus_to_use = (
                range(torch.cuda.device_count())
                if torch.cuda.is_available()
                else range(1)
            )

        logger.info(
            f"Loading SAM3 video model from {model_path} on devices {gpus_to_use}"
        )
        self.predictor = build_sam3_video_predictor(
            gpus_to_use=gpus_to_use,
            bpe_path=bpe_path,
            checkpoint_path=model_path,
        )

        logger.info("SAM3 video model loaded successfully")

        if hasattr(self.predictor, "model") and hasattr(self.predictor.model, "model"):
            model = self.predictor.model.model
            for name, param in model.named_parameters():
                if param.dtype != torch.float32 and "bias" in name:
                    param.data = param.data.float()

    def predict(self, image: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute segmentation on single frame (not used for video).

        Args:
            image: Input image in BGR format.
            params: Inference parameters.

        Returns:
            Dictionary with empty shapes (video requires session-based API).
        """
        logger.warning(
            "Single frame predict called on video model. "
            "Use video API endpoints instead."
        )
        return {"shapes": [], "description": ""}

    def init_session(
        self, frames: List[np.ndarray], start_frame_index: int
    ) -> Dict[str, Any]:
        """Initialize a new video session.

        Args:
            frames: List of video frames as numpy arrays.
            start_frame_index: Starting frame index in original sequence.

        Returns:
            Dictionary with session_id, num_frames, start_frame_index.
        """
        with self._sessions_lock:
            if len(self._sessions) >= self._max_sessions:
                self._cleanup_oldest_session()

            session_id = str(uuid.uuid4())

            if session_id in self._sessions:
                logger.warning(f"Session {session_id} already exists, cleaning up")
                self._sessions[session_id].cleanup()

            session = _VideoSession(
                session_id, frames, start_frame_index, self.predictor
            )
            self._sessions[session_id] = session

        return {
            "session_id": session_id,
            "num_frames": len(frames),
            "start_frame_index": start_frame_index,
        }

    def add_prompt(
        self,
        session_id: str,
        text_prompt: str,
        frame_index: int,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Add text prompt to a video frame.

        Args:
            session_id: Session identifier.
            text_prompt: Text prompt string.
            frame_index: Frame index to add prompt to.
            params: Additional parameters (conf_threshold, show_boxes, etc.).

        Returns:
            Dictionary with frame_index, masks list, and num_objects.
        """
        session = self._get_session(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}

        relative_frame_index = frame_index - session.start_frame_index
        if relative_frame_index < 0 or relative_frame_index >= len(session.frames):
            return {"error": f"Frame index {frame_index} out of range"}

        session.predictor.handle_request(
            request=dict(
                type="reset_session",
                session_id=session_id,
            )
        )

        response = session.predictor.handle_request(
            request=dict(
                type="add_prompt",
                session_id=session_id,
                frame_index=relative_frame_index,
                text=text_prompt.rstrip("."),
            )
        )

        outputs = response.get("outputs", {})
        if not isinstance(outputs, dict):
            logger.error(f"Unexpected outputs format: {type(outputs)}")
            return {"error": f"Unexpected outputs format: {type(outputs)}"}

        out_binary_masks = outputs.get("out_binary_masks", [])
        out_probs = outputs.get("out_probs", [])
        out_obj_ids = self._normalize_obj_ids(outputs.get("out_obj_ids", []))
        out_boxes_xywh = outputs.get("out_boxes_xywh", [])

        if len(out_binary_masks) == 0:
            logger.warning("No masks returned from video prompt")
            return {"frame_index": frame_index, "masks": [], "num_objects": 0}

        session.text_prompt = text_prompt
        session.last_prompt_frame = frame_index
        session.prompt_frame_outputs = {
            "out_binary_masks": out_binary_masks,
            "out_probs": out_probs,
            "out_obj_ids": out_obj_ids,
            "out_boxes_xywh": out_boxes_xywh,
        }
        session.prompt_frame_params = params.copy()

        inference_params = self._get_inference_params(params)
        orig_height, orig_width = self._get_frame_dimensions(session.frames)

        shapes = self._convert_outputs_to_shapes(
            out_binary_masks,
            out_probs,
            out_obj_ids,
            out_boxes_xywh,
            text_prompt,
            inference_params["conf_threshold"],
            inference_params["show_boxes"],
            inference_params["show_masks"],
            inference_params["epsilon_factor"],
            orig_width,
            orig_height,
        )

        return {
            "frame_index": frame_index,
            "masks": shapes,
            "num_objects": len(shapes),
        }

    def add_point_prompt(
        self,
        session_id: str,
        points: List[List[float]],
        point_labels: List[int],
        obj_id: Optional[int],
        frame_index: int,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Add point prompt to a video frame.

        Args:
            session_id: Session identifier.
            points: List of point coordinates in relative format (N, 2).
            point_labels: List of point labels (1 for positive, 0 for negative).
            obj_id: Object ID for the prompt.
            frame_index: Frame index to add prompt to.
            params: Additional parameters (conf_threshold, show_boxes, etc.).

        Returns:
            Dictionary with frame_index, masks list, and num_objects.
        """
        session = self._get_session(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}

        relative_frame_index = frame_index - session.start_frame_index
        if relative_frame_index < 0 or relative_frame_index >= len(session.frames):
            return {"error": f"Frame index {frame_index} out of range"}

        if not points or not point_labels:
            return {"error": "Points and point_labels are required"}

        if len(points) != len(point_labels):
            return {"error": "Points and point_labels must have same length"}

        if obj_id is None:
            obj_id = 99999

        try:
            predictor_session = session.predictor._get_session(session_id)
            inference_state = predictor_session["state"]
            if (
                "cached_frame_outputs" not in inference_state
                or relative_frame_index not in inference_state["cached_frame_outputs"]
            ):
                if "cached_frame_outputs" not in inference_state:
                    inference_state["cached_frame_outputs"] = {}
                inference_state["cached_frame_outputs"][relative_frame_index] = {}
        except (AttributeError, RuntimeError, KeyError) as e:
            logger.warning(
                f"Could not initialize cache for frame {relative_frame_index}: {e}"
            )

        response = session.predictor.handle_request(
            request=dict(
                type="add_prompt",
                session_id=session_id,
                frame_index=relative_frame_index,
                points=points,
                point_labels=point_labels,
                obj_id=obj_id,
            )
        )

        outputs = response.get("outputs", {})
        if not isinstance(outputs, dict):
            logger.error(f"Unexpected outputs format: {type(outputs)}")
            return {"error": f"Unexpected outputs format: {type(outputs)}"}

        out_binary_masks = outputs.get("out_binary_masks", [])
        out_probs = outputs.get("out_probs", [])
        out_obj_ids = self._normalize_obj_ids(outputs.get("out_obj_ids", []))
        out_boxes_xywh = outputs.get("out_boxes_xywh", [])

        if len(out_binary_masks) == 0:
            logger.warning("No masks returned from video point prompt")
            return {"frame_index": frame_index, "masks": [], "num_objects": 0}

        try:
            predictor_session = session.predictor._get_session(session_id)
            inference_state = predictor_session["state"]
            if "cached_frame_outputs" not in inference_state:
                inference_state["cached_frame_outputs"] = {}

            num_frames = len(session.frames)
            obj_id_to_mask = {}

            if len(out_obj_ids) > 0:
                import torch
                import torch.nn.functional as F

                H_video = inference_state.get("orig_height", session.frames[0].shape[0])
                W_video = inference_state.get("orig_width", session.frames[0].shape[1])

                for i, obj_id in enumerate(out_obj_ids):
                    obj_id_int = int(obj_id) if hasattr(obj_id, "__int__") else obj_id
                    if i < len(out_binary_masks):
                        mask = out_binary_masks[i]
                        if isinstance(mask, np.ndarray):
                            mask_tensor = torch.from_numpy(mask).float()
                        elif isinstance(mask, torch.Tensor):
                            mask_tensor = mask.float()
                        else:
                            mask_tensor = torch.tensor(mask, dtype=torch.float32)

                        if mask_tensor.dim() == 2:
                            mask_tensor = mask_tensor.unsqueeze(0).unsqueeze(0)
                        elif mask_tensor.dim() == 3:
                            mask_tensor = mask_tensor.unsqueeze(0)

                        if mask_tensor.shape[-2:] != (H_video, W_video):
                            mask_tensor = F.interpolate(
                                mask_tensor,
                                size=(H_video, W_video),
                                mode="bilinear",
                                align_corners=False,
                            )

                        mask_bool = mask_tensor.squeeze() > 0.0
                        if isinstance(mask_bool, torch.Tensor):
                            mask_bool = mask_bool.to(torch.bool)
                        obj_id_to_mask[obj_id_int] = mask_bool

            for fidx in range(num_frames):
                if fidx not in inference_state["cached_frame_outputs"]:
                    inference_state["cached_frame_outputs"][
                        fidx
                    ] = obj_id_to_mask.copy()
                else:
                    inference_state["cached_frame_outputs"][fidx].update(obj_id_to_mask)
        except (AttributeError, RuntimeError, KeyError, Exception) as e:
            logger.warning(f"Could not initialize cache for all frames: {e}")

        session.is_point_prompt = True
        session.last_prompt_frame = frame_index
        session.prompt_frame_outputs = {
            "out_binary_masks": out_binary_masks,
            "out_probs": out_probs,
            "out_obj_ids": out_obj_ids,
            "out_boxes_xywh": out_boxes_xywh,
        }
        session.prompt_frame_params = params.copy()

        inference_params = self._get_inference_params(params)
        orig_height, orig_width = self._get_frame_dimensions(session.frames)

        shapes = self._convert_outputs_to_shapes(
            out_binary_masks,
            out_probs,
            out_obj_ids,
            out_boxes_xywh,
            "AUTOLABEL_OBJECT",
            inference_params["conf_threshold"],
            inference_params["show_boxes"],
            inference_params["show_masks"],
            inference_params["epsilon_factor"],
            orig_width,
            orig_height,
        )

        return {
            "frame_index": frame_index,
            "masks": shapes,
            "num_objects": len(shapes),
        }

    def start_propagation(
        self,
        session_id: str,
        start_frame: Optional[int] = None,
        end_frame: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Start video propagation task.

        Args:
            session_id: Session identifier.
            start_frame: Optional start frame index (absolute).
            end_frame: Optional end frame index (absolute).

        Returns:
            Dictionary with task_id and status.
        """
        session = self._get_session(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}

        if not session.text_prompt and not session.is_point_prompt:
            return {"error": "No text prompt or point prompt set for session"}

        if start_frame is not None:
            start_frame = start_frame - session.start_frame_index
        if end_frame is not None:
            end_frame = end_frame - session.start_frame_index

        task_id = str(uuid.uuid4())
        task = _PropagationTask(task_id, session_id, start_frame, end_frame)

        with self._tasks_lock:
            self._tasks[task_id] = task

        logger.info(
            f"Submitting propagation task: task_id={task_id}, "
            f"session_id={session_id}"
        )

        try:
            future = self._executor.submit(self._run_propagation, task, session)

            def log_exception(fut):
                try:
                    fut.result()
                except Exception as e:
                    logger.error(
                        f"Propagation task {task_id} raised exception: {e}",
                        exc_info=True,
                    )

            future.add_done_callback(log_exception)
        except Exception as e:
            logger.error(f"Failed to submit propagation task {task_id}: {e}")
            with self._tasks_lock:
                task.status = _TaskStatus.FAILED
                task.error = f"Failed to submit task: {str(e)}"
            return {"error": str(e)}

        return {"task_id": task_id, "status": "processing"}

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get propagation task status.

        Args:
            task_id: Task identifier.

        Returns:
            Dictionary with status, progress, and results if completed.
        """
        with self._tasks_lock:
            task = self._tasks.get(task_id)

        if not task:
            return {"error": f"Task {task_id} not found"}

        session = self._get_session(task.session_id)
        start_frame_offset = session.start_frame_index if session else 0

        response_data = {
            "status": task.status.value,
            "progress": task.progress,
            "current_frame": (
                task.current_frame + start_frame_offset if task.current_frame else 0
            ),
            "total_frames": task.total_frames,
        }

        if task.status == _TaskStatus.COMPLETED:
            results = self._build_completed_results(task, session)
            response_data["results"] = results
        elif task.status == _TaskStatus.FAILED:
            response_data["error"] = task.error

        return response_data

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel propagation task.

        Args:
            task_id: Task identifier.

        Returns:
            Dictionary with success message or error.
        """
        with self._tasks_lock:
            task = self._tasks.get(task_id)
            if task:
                task.cancel()
                return {"message": "Task cancelled"}
            return {"error": f"Task {task_id} not found"}

    def propagate_stream(
        self,
        session_id: str,
        start_frame: Optional[int] = None,
        end_frame: Optional[int] = None,
    ):
        """Stream video propagation results (generator for SSE).

        Args:
            session_id: Session identifier.
            start_frame: Optional start frame index (absolute).
            end_frame: Optional end frame index (absolute).

        Yields:
            Dictionary events with type, progress, and results.
        """
        session = self._get_session(session_id)
        if not session:
            yield {
                "type": "error",
                "message": f"Session {session_id} not found",
            }
            return

        if not session.text_prompt and not session.is_point_prompt:
            yield {
                "type": "error",
                "message": "No text prompt or point prompt set for session",
            }
            return

        rel_start = None
        rel_end = None
        if start_frame is not None:
            rel_start = start_frame - session.start_frame_index
        if end_frame is not None:
            rel_end = end_frame - session.start_frame_index

        total_frames = len(session.frames)
        start_frame_offset = session.start_frame_index
        orig_height, orig_width = self._get_frame_dimensions(session.frames)
        text_prompt = session.text_prompt if session.text_prompt else "AUTOLABEL_OBJECT"

        yield {
            "type": "started",
            "total_frames": total_frames,
            "start_frame_index": start_frame_offset,
        }

        request_dict = dict(
            type="propagate_in_video",
            session_id=session_id,
            propagation_direction="forward",
        )
        if rel_start is not None:
            request_dict["start_frame_index"] = rel_start
        if rel_end is not None:
            request_dict["max_frame_num_to_track"] = rel_end

        bf16_context = None
        try:
            if torch.cuda.is_available():
                current_device = torch.cuda.current_device()
                torch.cuda.set_device(current_device)
                bf16_context = torch.autocast(device_type="cuda", dtype=torch.bfloat16)
                bf16_context.__enter__()

            generator = session.predictor.handle_stream_request(request=request_dict)

            prompt_frame_relative_idx = None
            prompt_absolute_idx = None
            if session.last_prompt_frame is not None:
                prompt_frame_relative_idx = (
                    session.last_prompt_frame - session.start_frame_index
                )
                prompt_absolute_idx = session.last_prompt_frame

            frame_count = 0
            results = {}

            for response in generator:
                frame_idx = response.get("frame_index")
                outputs = response.get("outputs")

                if frame_idx is None or outputs is None:
                    continue

                frame_count += 1
                absolute_frame_idx = frame_idx + start_frame_offset

                yield {
                    "type": "progress",
                    "current_frame": absolute_frame_idx,
                    "total_frames": total_frames,
                    "progress": frame_count / total_frames,
                }

                if (
                    prompt_frame_relative_idx is not None
                    and frame_idx == prompt_frame_relative_idx
                    and session.prompt_frame_outputs is not None
                ):
                    continue

                out_binary_masks = outputs.get("out_binary_masks", [])
                out_probs = outputs.get("out_probs", [])
                out_obj_ids = self._normalize_obj_ids(outputs.get("out_obj_ids", []))
                out_boxes_xywh = outputs.get("out_boxes_xywh", [])

                params = self._get_inference_params(session.prompt_frame_params)
                shapes = self._convert_outputs_to_shapes(
                    out_binary_masks,
                    out_probs,
                    out_obj_ids,
                    out_boxes_xywh,
                    text_prompt,
                    params["conf_threshold"],
                    params["show_boxes"],
                    params["show_masks"],
                    params["epsilon_factor"],
                    orig_width,
                    orig_height,
                )

                results[absolute_frame_idx] = {"masks": shapes}

            if (
                session.prompt_frame_outputs is not None
                and prompt_absolute_idx is not None
            ):
                prompt_outputs = session.prompt_frame_outputs
                prompt_obj_ids = self._normalize_obj_ids(
                    prompt_outputs.get("out_obj_ids", [])
                )

                params = self._get_inference_params(session.prompt_frame_params)
                prompt_shapes = self._convert_outputs_to_shapes(
                    prompt_outputs.get("out_binary_masks", []),
                    prompt_outputs.get("out_probs", []),
                    prompt_obj_ids,
                    prompt_outputs.get("out_boxes_xywh", []),
                    text_prompt,
                    params["conf_threshold"],
                    params["show_boxes"],
                    params["show_masks"],
                    params["epsilon_factor"],
                    orig_width,
                    orig_height,
                )
                results[prompt_absolute_idx] = {"masks": prompt_shapes}

            yield {
                "type": "completed",
                "results": results,
            }

        except Exception as e:
            logger.error(f"Stream propagation error: {e}", exc_info=True)
            yield {"type": "error", "message": str(e)}
        finally:
            if bf16_context is not None:
                try:
                    bf16_context.__exit__(None, None, None)
                except Exception:
                    pass

    def cleanup_session(self, session_id: str) -> bool:
        """Clean up and remove a session.

        Args:
            session_id: Session identifier.

        Returns:
            True if session was removed, False if not found.
        """
        with self._sessions_lock:
            session = self._sessions.pop(session_id, None)
            if session:
                session.cleanup()
                return True
            return False

    def unload(self):
        """Release model resources."""
        with self._sessions_lock:
            for session in list(self._sessions.values()):
                session.cleanup()
            self._sessions.clear()

        with self._tasks_lock:
            for task in self._tasks.values():
                task.cancel()
        self._executor.shutdown(wait=True)
        self._tasks.clear()

        if hasattr(self, "predictor") and self.predictor:
            self.predictor.shutdown()
            del self.predictor
        logger.info("SAM3 video model unloaded")

    def _get_session(self, session_id: str) -> Optional[_VideoSession]:
        """Get session by ID with timeout check.

        Args:
            session_id: Session identifier.

        Returns:
            VideoSession instance or None if not found/expired.
        """
        with self._sessions_lock:
            session = self._sessions.get(session_id)
            if session:
                if time.time() - session.created_at > self._session_timeout:
                    logger.warning(f"Session {session_id} expired")
                    session.cleanup()
                    del self._sessions[session_id]
                    return None
            return session

    def _cleanup_oldest_session(self):
        """Remove oldest session to make room for new one."""
        if not self._sessions:
            return

        oldest_id = min(
            self._sessions.keys(),
            key=lambda sid: self._sessions[sid].created_at,
        )
        logger.info(f"Cleaning up oldest session {oldest_id} to make room")
        session = self._sessions.pop(oldest_id, None)
        if session:
            session.cleanup()

    def _run_propagation(self, task: _PropagationTask, session: _VideoSession):
        """Run propagation task in background thread.

        Args:
            task: Propagation task instance.
            session: Video session instance.
        """
        logger.info(
            f"[TASK START] Propagation task started: "
            f"task_id={task.task_id}, "
            f"thread_id={threading.current_thread().ident}"
        )

        try:
            with task.lock:
                if task._cancelled:
                    logger.info(f"Task {task.task_id} was cancelled before starting")
                    return
                task.status = _TaskStatus.PROCESSING

            total_frames = len(session.frames)
            with task.lock:
                task.total_frames = total_frames

            logger.info(
                f"Starting propagation for task {task.task_id}, "
                f"total_frames={total_frames}"
            )

            outputs_per_frame = {}
            frame_count = 0

            request_dict = dict(
                type="propagate_in_video",
                session_id=task.session_id,
                propagation_direction="forward",
            )
            if task.start_frame is not None:
                request_dict["start_frame_index"] = task.start_frame
            if task.end_frame is not None:
                request_dict["max_frame_num_to_track"] = task.end_frame

            bf16_context = None
            if torch.cuda.is_available():
                current_device = torch.cuda.current_device()
                torch.cuda.set_device(current_device)
                bf16_context = torch.autocast(device_type="cuda", dtype=torch.bfloat16)
                bf16_context.__enter__()

            generator = session.predictor.handle_stream_request(request=request_dict)

            for response in generator:
                with task.lock:
                    if task._cancelled:
                        task.status = _TaskStatus.CANCELLED
                        logger.info(f"Task {task.task_id} was cancelled")
                        if bf16_context is not None:
                            try:
                                bf16_context.__exit__(None, None, None)
                            except Exception:
                                pass
                        return

                frame_idx = response.get("frame_index")
                outputs = response.get("outputs")

                if frame_idx is None or outputs is None:
                    continue

                outputs_per_frame[frame_idx] = outputs

                frame_count += 1
                with task.lock:
                    task.current_frame = frame_idx
                    task.progress = (
                        frame_count / total_frames if total_frames > 0 else 0.0
                    )

            logger.info(
                f"Propagation finished for task {task.task_id}, "
                f"collected {len(outputs_per_frame)} frame results"
            )

            with task.lock:
                task.results = outputs_per_frame
                task.status = _TaskStatus.COMPLETED
                task.progress = 1.0

        except Exception as e:
            logger.error(f"Propagation task {task.task_id} failed: {e}", exc_info=True)
            with task.lock:
                task.status = _TaskStatus.FAILED
                task.error = str(e)
        finally:
            if bf16_context is not None:
                try:
                    bf16_context.__exit__(None, None, None)
                except Exception:
                    pass

    def _build_completed_results(
        self, task: _PropagationTask, session: Optional[_VideoSession]
    ) -> Dict[int, Dict[str, Any]]:
        """Build results dictionary for completed task.

        Args:
            task: Completed propagation task.
            session: Video session instance.

        Returns:
            Dictionary mapping frame index to masks.
        """
        results = {}
        start_frame_offset = session.start_frame_index if session else 0
        orig_height, orig_width = self._get_frame_dimensions(
            session.frames if session else None
        )
        text_prompt = session.text_prompt if session else "AUTOLABEL_OBJECT"

        prompt_frame_relative_idx = None
        prompt_absolute_idx = None
        if session and session.last_prompt_frame is not None:
            prompt_frame_relative_idx = (
                session.last_prompt_frame - session.start_frame_index
            )
            prompt_absolute_idx = session.last_prompt_frame

        for frame_idx, outputs in task.results.items():
            absolute_frame_idx = frame_idx + start_frame_offset

            if (
                prompt_frame_relative_idx is not None
                and frame_idx == prompt_frame_relative_idx
                and session
                and session.prompt_frame_outputs is not None
            ):
                continue

            out_binary_masks = outputs.get("out_binary_masks", [])
            out_probs = outputs.get("out_probs", [])
            out_obj_ids = self._normalize_obj_ids(outputs.get("out_obj_ids", []))
            out_boxes_xywh = outputs.get("out_boxes_xywh", [])

            params = self._get_inference_params(
                session.prompt_frame_params if session else None
            )
            shapes = self._convert_outputs_to_shapes(
                out_binary_masks,
                out_probs,
                out_obj_ids,
                out_boxes_xywh,
                text_prompt,
                params["conf_threshold"],
                params["show_boxes"],
                params["show_masks"],
                params["epsilon_factor"],
                orig_width,
                orig_height,
            )

            results[absolute_frame_idx] = {"masks": shapes}

        if (
            session
            and session.prompt_frame_outputs is not None
            and prompt_absolute_idx is not None
        ):
            prompt_outputs = session.prompt_frame_outputs
            prompt_obj_ids = self._normalize_obj_ids(
                prompt_outputs.get("out_obj_ids", [])
            )

            params = self._get_inference_params(session.prompt_frame_params)
            prompt_shapes = self._convert_outputs_to_shapes(
                prompt_outputs.get("out_binary_masks", []),
                prompt_outputs.get("out_probs", []),
                prompt_obj_ids,
                prompt_outputs.get("out_boxes_xywh", []),
                text_prompt,
                params["conf_threshold"],
                params["show_boxes"],
                params["show_masks"],
                params["epsilon_factor"],
                orig_width,
                orig_height,
            )
            results[prompt_absolute_idx] = {"masks": prompt_shapes}

        return results

    def _get_inference_params(
        self, prompt_params: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract inference parameters from prompt params or defaults.

        Args:
            prompt_params: Optional prompt frame parameters dictionary.

        Returns:
            Dictionary with conf_threshold, show_boxes, show_masks, epsilon_factor.
        """
        params = prompt_params or {}
        return {
            "conf_threshold": params.get(
                "conf_threshold", self.params.get("conf_threshold", 0.25)
            ),
            "show_boxes": params.get("show_boxes", self.params.get("show_boxes", True)),
            "show_masks": params.get(
                "show_masks", self.params.get("show_masks", False)
            ),
            "epsilon_factor": params.get(
                "epsilon_factor", self.params.get("epsilon_factor", 0.001)
            ),
        }

    def _get_frame_dimensions(
        self, frames: Optional[List[np.ndarray]]
    ) -> Tuple[int, int]:
        """Get frame dimensions from frames list.

        Args:
            frames: Optional list of video frames.

        Returns:
            Tuple of (height, width) or default (1080, 1920).
        """
        if frames and len(frames) > 0:
            return len(frames[0]), len(frames[0][0])
        return 1080, 1920

    def _normalize_obj_ids(self, obj_ids: Any) -> np.ndarray:
        """Normalize object IDs to numpy array.

        Args:
            obj_ids: Object IDs in various formats.

        Returns:
            Numpy array of object IDs.
        """
        if isinstance(obj_ids, np.ndarray):
            return obj_ids
        elif isinstance(obj_ids, (list, tuple)):
            return np.array(obj_ids) if obj_ids else np.array([])
        else:
            return np.array([])

    def _convert_outputs_to_shapes(
        self,
        out_binary_masks: np.ndarray,
        out_probs: np.ndarray,
        out_obj_ids: np.ndarray,
        out_boxes_xywh: np.ndarray,
        text_prompt: str,
        conf_threshold: float,
        show_boxes: bool,
        show_masks: bool,
        epsilon_factor: float,
        orig_width: int,
        orig_height: int,
    ) -> List[Dict[str, Any]]:
        """Convert SAM3 video outputs to shape dictionaries.

        Args:
            out_binary_masks: Binary masks array (N, H, W).
            out_probs: Confidence scores array (N,).
            out_obj_ids: Object IDs array (N,).
            out_boxes_xywh: Boxes in normalized xywh format (N, 4).
            text_prompt: Text prompt string.
            conf_threshold: Confidence threshold.
            show_boxes: Whether to return bounding boxes.
            show_masks: Whether to return masks as polygons.
            epsilon_factor: Factor for polygon approximation.
            orig_width: Original image width.
            orig_height: Original image height.

        Returns:
            List of shape dictionaries.
        """
        shapes = []

        if isinstance(out_binary_masks, (list, tuple)):
            if len(out_binary_masks) == 0:
                return shapes
        elif isinstance(out_binary_masks, np.ndarray):
            if out_binary_masks.size == 0:
                return shapes

        out_obj_ids = self._normalize_obj_ids(out_obj_ids)

        num_objects = (
            len(out_binary_masks)
            if isinstance(out_binary_masks, (list, np.ndarray))
            else 0
        )
        if num_objects == 0:
            return shapes

        for i in range(num_objects):
            try:
                prob = float(out_probs[i])
                if prob < conf_threshold:
                    continue
                score = prob
            except (IndexError, TypeError, ValueError):
                score = 1.0

            if text_prompt:
                label = text_prompt
            else:
                label = "AUTOLABEL_OBJECT"
                score = None

            mask = out_binary_masks[i]
            if isinstance(mask, np.ndarray):
                mask_np = mask.astype(np.float32)
            else:
                mask_np = np.array(mask, dtype=np.float32)

            group_id = None
            if i < len(out_obj_ids):
                try:
                    obj_id = int(out_obj_ids[i])
                    group_id = obj_id + 1
                except (ValueError, TypeError, IndexError):
                    pass

            if show_masks:
                points = self._mask_to_polygon(mask_np, epsilon_factor)
                if points:
                    shapes.append(
                        {
                            "label": label,
                            "shape_type": "polygon",
                            "points": points,
                            "score": score,
                            "group_id": group_id,
                        }
                    )

            if show_boxes:
                try:
                    box_xywh = out_boxes_xywh[i]
                except (IndexError, TypeError):
                    continue

                x_norm, y_norm, w_norm, h_norm = box_xywh
                x_min = float(x_norm * orig_width)
                y_min = float(y_norm * orig_height)
                x_max = float((x_norm + w_norm) * orig_width)
                y_max = float((y_norm + h_norm) * orig_height)

                shapes.append(
                    {
                        "label": label,
                        "shape_type": "rectangle",
                        "points": [
                            [x_min, y_min],
                            [x_max, y_min],
                            [x_max, y_max],
                            [x_min, y_max],
                        ],
                        "score": score,
                        "group_id": group_id,
                    }
                )

        return shapes

    def _mask_to_polygon(
        self, mask: np.ndarray, epsilon_factor: float = 0.001
    ) -> List[List[float]]:
        """Convert binary mask to polygon points.

        Args:
            mask: Binary mask array.
            epsilon_factor: Factor for polygon approximation epsilon.

        Returns:
            List of polygon points.
        """
        mask_uint8 = (mask > 0.5).astype(np.uint8)
        contours, _ = cv2.findContours(
            mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return []

        largest_contour = max(contours, key=cv2.contourArea)
        if epsilon_factor > 0:
            epsilon = epsilon_factor * cv2.arcLength(largest_contour, True)
            approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        else:
            approx = largest_contour

        points = []
        for point in approx:
            x, y = point[0]
            points.append([float(x), float(y)])

        if points and points[0] != points[-1]:
            points.append(points[0])

        return points
