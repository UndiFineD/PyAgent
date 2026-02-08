# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_withoutbg.py\src.py\withoutbg.py\core_1feec2abbfcb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\src\withoutbg\core.py

"""Core background removal functionality."""

from pathlib import Path

from typing import Any, Optional, Union

from PIL import Image

from .api import StudioAPI

from .exceptions import WithoutBGError

from .models import SnapModel


def remove_background(
    input_image: Union[str, Path, Image.Image, bytes],
    output_path: Optional[Union[str, Path]] = None,
    api_key: Optional[str] = None,
    model_name: str = "snap",
    **kwargs: Any,
) -> Image.Image:
    """Remove background from an image.

    Args:

        input_image: Input image as file path, PIL Image, or bytes

        output_path: Optional path to save the result

        api_key: API key for Studio service (uses local Snap model if None)

        model_name: Model to use ("snap" for local, "studio" for API)

        **kwargs: Additional arguments passed to the model/API

    Returns:

        PIL Image with background removed

    Examples:

        >>> # Local processing with Snap model

        >>> result = remove_background("input.jpg")

        >>> # Cloud processing with Studio API

        >>> result = remove_background("input.jpg", api_key="sk_...")

        >>> # Save result directly

        >>> remove_background("input.jpg", output_path="output.png")

    """

    try:
        if api_key or model_name == "studio":
            # Use Studio API

            api = StudioAPI(api_key)

            result = api.remove_background(input_image, **kwargs)

        else:
            # Use local Snap model

            model = SnapModel()

            result = model.remove_background(input_image, **kwargs)

        if output_path:
            result.save(output_path)

        return result

    except Exception as e:
        raise WithoutBGError(f"Background removal failed: {str(e)}") from e


def remove_background_batch(
    input_images: list[Union[str, Path, Image.Image, bytes]],
    output_dir: Optional[Union[str, Path]] = None,
    api_key: Optional[str] = None,
    model_name: str = "snap",
    **kwargs: Any,
) -> list[Image.Image]:
    """Remove background from multiple images.

    Args:

        input_images: List of input images

        output_dir: Directory to save results (optional)

        api_key: API key for Studio service

        model_name: Model to use

        **kwargs: Additional arguments

    Returns:

        List of PIL Images with backgrounds removed

    """

    results = []

    for i, input_image in enumerate(input_images):
        output_path = None

        if output_dir:
            output_dir = Path(output_dir)

            output_dir.mkdir(parents=True, exist_ok=True)

            # Try to get original filename

            if isinstance(input_image, (str, Path)):
                input_path = Path(input_image)

                stem = input_path.stem

                suffix = input_path.suffix or ".png"

                output_filename = f"{stem}-withoutbg{suffix}"

            else:
                # For PIL Images or bytes, use numbered fallback

                output_filename = f"output_{i:04d}-withoutbg.png"

            output_path = output_dir / output_filename

        result = remove_background(
            input_image,
            output_path=output_path,
            api_key=api_key,
            model_name=model_name,
            **kwargs,
        )

        results.append(result)

    return results
