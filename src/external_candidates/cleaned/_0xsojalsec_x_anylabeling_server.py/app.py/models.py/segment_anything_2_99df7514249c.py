# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\models\segment_anything_2.py
import threading
from collections import OrderedDict
from hashlib import md5
from typing import Any, Dict, List

import numpy as np
import torch
from app.core.registry import register_model
from app.schemas.shape import Shape
from loguru import logger
from PIL import Image

from . import BaseModel


class LRUCache:
    """Thread-safe LRU cache implementation."""

    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.lock = threading.Lock()
        self._cache = OrderedDict()

    def get(self, key):
        """Get value from cache. Returns None if key is not present."""
        with self.lock:
            if key not in self._cache:
                return None
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(self, key, value):
        """Put value into cache. If cache is full, oldest item is evicted."""
        with self.lock:
            self._cache[key] = value
            self._cache.move_to_end(key)
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)


@register_model("segment_anything_2")
class SegmentAnything2(BaseModel):
    """Segment Anything Model 2 for image segmentation with point or box prompts."""

    def load(self):
        """Load SAM2 model and initialize components."""
        import os
        import sys

        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

        sam2_parent_dir = os.path.join(os.path.dirname(__file__))
        if sam2_parent_dir not in sys.path:
            sys.path.insert(0, sam2_parent_dir)

        from sam2.build_sam import build_sam2
        from sam2.sam2_image_predictor import SAM2ImagePredictor

        model_cfg = os.path.join("configs/sam2.1", self.params.get("model_cfg") + ".yaml")
        checkpoint_path = self.params.get("model_path")
        device = self.params.get("device", "cuda")

        # select the device for computation
        if torch.cuda.is_available() and "cuda" in device:
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available() and "mps" in device:
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        if self.device.type == "cuda":
            # use bfloat16 for the entire notebook
            torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
            # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
            if torch.cuda.get_device_properties(0).major >= 8:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
        elif device.type == "mps":
            print(
                "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
                "give numerically different outputs and sometimes degraded performance on MPS. "
                "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
            )

        logger.info(f"model_cfg: {model_cfg}, device: {self.device}, Loading SAM2 model from {checkpoint_path}")
        sam2_model = build_sam2(model_cfg, checkpoint_path, device=self.device)
        self.predictor = SAM2ImagePredictor(sam2_model)

        cache_size = self.params.get("cache_size", 10)
        self.image_embedding_cache = LRUCache(maxsize=cache_size)
        logger.info(f"SAM2 model loaded successfully with embedding cache size: {cache_size}")

    def predict(self, image: np.ndarray, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute segmentation based on point or box prompts.

        Args:
            image: Input image in BGR format.
            params: Inference parameters including marks.

        Returns:
            Dictionary with shapes and description.
        """
        marks = params.get("marks", [])

        if not marks:
            logger.warning("No prompts provided")
            return {"shapes": [], "description": "", "replace": False}

        return self._predict_with_marks(image, marks, params)

    def _predict_with_marks(
        self,
        image: np.ndarray,
        marks: List[Dict[str, Any]],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute segmentation with visual prompts.

        Args:
            image: Input image in BGR format.
            marks: List of visual prompts with type, label, and data fields.
            params: Inference parameters.

        Returns:
            Dictionary with shapes and description.
        """
        show_boxes = params.get("show_boxes", self.params.get("show_boxes", False))
        show_masks = params.get("show_masks", self.params.get("show_masks", True))
        multimask_output = params.get("multimask_output", self.params.get("multimask_output", False))

        point_coords = []
        point_labels = []
        box_coords = None

        logger.info(f"Processing visual prompts: {len(marks)} marks")

        for mark in marks:
            mark_type = mark.get("type")
            if mark_type == "point":
                data = mark.get("data", [])
                if len(data) == 2:
                    point_coords.append(data)
                    label = mark.get("label", 1)
                    point_labels.append(label)
            elif mark_type == "rectangle":
                data = mark.get("data", [])
                if len(data) == 4:
                    x1, y1, x2, y2 = data
                    if box_coords is None:
                        box_coords = []
                    box_coords.append([x1, y1, x2, y2])

        if not point_coords and box_coords is None:
            logger.warning("No valid prompts provided")
            return {"shapes": [], "description": "", "replace": False}

        image_key = self._get_image_key(image, params)
        cached_data = self.image_embedding_cache.get(image_key)

        pil_image = Image.fromarray(image[:, :, ::-1])
        image_array = np.array(pil_image)
        image_hw = tuple(image_array.shape[:2])

        if cached_data is not None:
            logger.debug(f"Using cached embedding data...")
            cached_features, cached_orig_hw = cached_data
            if cached_orig_hw == image_hw:
                self.predictor._features = {
                    "image_embed": cached_features["image_embed"].clone(),
                    "high_res_feats": [feat.clone() for feat in cached_features["high_res_feats"]],
                }
                self.predictor._orig_hw = [cached_orig_hw]
                self.predictor._is_image_set = True
            else:
                self.predictor.set_image(image_array)
                embedding_data = (
                    {
                        "image_embed": self.predictor._features["image_embed"].clone(),
                        "high_res_feats": [feat.clone() for feat in self.predictor._features["high_res_feats"]],
                    },
                    self.predictor._orig_hw[0],
                )
                self.image_embedding_cache.put(image_key, embedding_data)
        else:
            logger.debug(f"Extracting new embedding data...")
            self.predictor.set_image(image_array)
            embedding_data = (
                {
                    "image_embed": self.predictor._features["image_embed"].clone(),
                    "high_res_feats": [feat.clone() for feat in self.predictor._features["high_res_feats"]],
                },
                self.predictor._orig_hw[0],
            )
            self.image_embedding_cache.put(image_key, embedding_data)

        if point_coords:
            point_coords = np.array(point_coords)
            point_labels = np.array(point_labels)
        else:
            point_coords = None
            point_labels = None

        if box_coords is not None:
            box_coords = np.array(box_coords)
            if len(box_coords.shape) == 1:
                box_coords = box_coords[None, :]
            elif len(box_coords.shape) == 2 and box_coords.shape[0] == 1:
                box_coords = box_coords[None, :]

        masks, scores, _ = self.predictor.predict(
            point_coords=point_coords,
            point_labels=point_labels,
            box=box_coords,
            multimask_output=multimask_output,
        )

        if len(masks) == 0:
            logger.warning("No masks predicted")
            return {"shapes": [], "description": "", "replace": False}

        if multimask_output:
            sorted_ind = np.argsort(scores)[::-1]
            masks = masks[sorted_ind]
            scores = scores[sorted_ind]
            best_mask = masks[0]
            best_score = scores[0]
        else:
            if len(masks.shape) == 3:
                best_mask = masks[0]
            else:
                best_mask = masks
            best_score = scores[0] if len(scores) > 0 else 1.0

        if isinstance(best_mask, torch.Tensor):
            best_mask = best_mask.cpu().numpy()
        if isinstance(best_score, torch.Tensor):
            best_score = best_score.cpu().item()

        epsilon_factor = params.get("epsilon_factor", self.params.get("epsilon_factor", 0.001))

        shapes = self._convert_results_to_shapes(
            best_mask,
            show_boxes,
            show_masks,
            epsilon_factor,
        )

        return {"shapes": shapes, "description": "", "replace": False}

    def _convert_results_to_shapes(
        self,
        mask: np.ndarray,
        show_boxes: bool = False,
        show_masks: bool = True,
        epsilon_factor: float = 0.001,
    ) -> List[Shape]:
        """Convert SAM2 results to Shape objects.

        Args:
            mask: Binary mask array.
            show_boxes: Whether to return bounding boxes.
            show_masks: Whether to return masks as polygons.
            epsilon_factor: Factor for polygon approximation epsilon.

        Returns:
            List of Shape objects.
        """
        import cv2

        shapes = []

        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()

        mask_uint8 = (mask > 0.5).astype(np.uint8)
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours:
            return []

        approx_contours = []
        for contour in contours:
            epsilon = epsilon_factor * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            approx_contours.append(approx)

        if len(approx_contours) > 1:
            image_size = mask_uint8.shape[0] * mask_uint8.shape[1]
            areas = [cv2.contourArea(contour) for contour in approx_contours]
            filtered_approx_contours = [
                contour for contour, area in zip(approx_contours, areas) if area < image_size * 0.9
            ]
            if filtered_approx_contours:
                approx_contours = filtered_approx_contours

        if len(approx_contours) > 1:
            areas = [cv2.contourArea(contour) for contour in approx_contours]
            avg_area = np.mean(areas)
            filtered_approx_contours = [
                contour for contour, area in zip(approx_contours, areas) if area > avg_area * 0.2
            ]
            if filtered_approx_contours:
                approx_contours = filtered_approx_contours

        if show_masks:
            for approx in approx_contours:
                points = approx.reshape(-1, 2).tolist()
                if len(points) < 3:
                    continue
                if points[0] != points[-1]:
                    points.append(points[0])

                shape = Shape(
                    label="AUTOLABEL_OBJECT",
                    shape_type="polygon",
                    points=[[float(p[0]), float(p[1])] for p in points],
                )
                shapes.append(shape)

        if show_boxes:
            x_min = float("inf")
            y_min = float("inf")
            x_max = 0.0
            y_max = 0.0

            for approx in approx_contours:
                points = approx.reshape(-1, 2)
                for point in points:
                    x, y = float(point[0]), float(point[1])
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)

            if x_min < x_max and y_min < y_max:
                shape = Shape(
                    label="AUTOLABEL_OBJECT",
                    shape_type="rectangle",
                    points=[
                        [x_min, y_min],
                        [x_max, y_min],
                        [x_max, y_max],
                        [x_min, y_max],
                    ],
                )
                shapes.append(shape)

        return shapes

    def _get_image_key(self, image: np.ndarray, params: Dict[str, Any]) -> str:
        """Get unique identifier for image.

        Args:
            image: Input image array.
            params: Inference parameters.

        Returns:
            Unique key for the image combining user identifier and content hash.
        """
        image_hash = md5(image.tobytes()).hexdigest()
        image_id = params.get("image_id")
        filename = params.get("filename")

        if image_id:
            return f"{image_id}_{image_hash}"
        if filename:
            return f"{filename}_{image_hash}"

        return f"hash_{image_hash}"

    def unload(self):
        """Release model resources."""
        if hasattr(self, "predictor"):
            del self.predictor
        if hasattr(self, "image_embedding_cache"):
            del self.image_embedding_cache
        logger.info("SAM2 model unloaded")
