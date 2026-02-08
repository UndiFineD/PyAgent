# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\src\withoutbg\cli.py
"""Command-line interface for withoutbg."""

import sys
from pathlib import Path
from typing import Any, Optional

import click
from click._termui_impl import ProgressBar
from PIL import Image

from . import __version__, remove_background
from .exceptions import WithoutBGError


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output file path (default: adds -withoutbg suffix)",
)
@click.option(
    "--api-key",
    envvar="WITHOUTBG_API_KEY",
    help="API key for Studio service (or set WITHOUTBG_API_KEY env var)",
)
@click.option("--use-api", is_flag=True, help="Use Studio API instead of local Snap model")
@click.option(
    "--model",
    default="snap",
    type=click.Choice(["snap", "studio"]),
    help="Model to use (snap=local, studio=API)",
)
@click.option(
    "--batch",
    is_flag=True,
    help="Process all images in directory (if input is directory)",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    help="Output directory for batch processing",
)
@click.option(
    "--format",
    type=click.Choice(["png", "jpg", "webp"]),
    default="png",
    help="Output image format",
)
@click.option("--quality", type=int, default=95, help="Output quality for JPEG (1-100)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.version_option(version=__version__)
def main(
    input_path: Path,
    output: Optional[Path],
    api_key: Optional[str],
    use_api: bool,
    model: str,
    batch: bool,
    output_dir: Optional[Path],
    format: str,
    quality: int,
    verbose: bool,
) -> None:
    """Remove background from images using AI.

    Examples:

        # Process single image with local Snap model
        withoutbg image.jpg

        # Use Studio API for best quality processing
        withoutbg image.jpg --use-api --api-key sk_...

        # Process all images in directory
        withoutbg photos/ --batch --output-dir results/

        # Specify output format and quality
        withoutbg image.jpg --format jpg --quality 90
    """

    try:
        # Determine if using API
        using_api = use_api or api_key or model == "studio"

        if using_api and not api_key:
            click.echo("Error: API key required when using Studio service", err=True)
            click.echo("Set WITHOUTBG_API_KEY environment variable or use --api-key", err=True)
            sys.exit(1)

        # Configure model
        actual_model = "studio" if using_api else "snap"

        if verbose:
            mode = "Studio API" if using_api else "Local Snap model"
            click.echo(f"Using {mode} for processing...")

        # Process images
        if batch or input_path.is_dir():
            _process_batch(input_path, output_dir, api_key, actual_model, format, quality, verbose)
        else:
            _process_single(input_path, output, api_key, actual_model, format, quality, verbose)

        if verbose:
            api_msg = ""
            if not using_api:
                api_msg = " (Want best quality? Try withoutbg.com)"
            click.echo(f"✅ Processing complete!{api_msg}")

    except WithoutBGError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n❌ Processing cancelled", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


def _process_single(
    input_path: Path,
    output_path: Optional[Path],
    api_key: Optional[str],
    model: str,
    format: str,
    quality: int,
    verbose: bool,
) -> None:
    """Process a single image."""

    if not output_path:
        # Generate output filename
        stem = input_path.stem
        output_path = input_path.parent / f"{stem}-withoutbg.{format}"

    if verbose:
        click.echo(f"Processing: {input_path}")
        click.echo(f"Output: {output_path}")

    # Remove background
    bar: ProgressBar
    with click.progressbar(length=1, label="Removing background") as bar:
        result = remove_background(input_path, api_key=api_key, model_name=model)
        bar.update(1)

    # Save result
    save_kwargs: dict[str, Any] = {}
    if format.lower() == "jpg":
        # Convert RGBA to RGB for JPEG
        if result.mode == "RGBA":
            background = Image.new("RGB", result.size, (255, 255, 255))
            background.paste(result, mask=result.split()[-1])  # Use alpha as mask
            result = background
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
    elif format.lower() == "webp":
        save_kwargs["quality"] = quality
        save_kwargs["method"] = 6  # Best compression

    # Map format names to PIL format strings
    pil_format = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}
    result.save(
        output_path,
        format=pil_format.get(format.lower(), format.upper()),
        **save_kwargs,
    )


def _process_batch(
    input_dir: Path,
    output_dir: Optional[Path],
    api_key: Optional[str],
    model: str,
    format: str,
    quality: int,
    verbose: bool,
) -> None:
    """Process multiple images in a directory."""

    # Find image files
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

    if input_dir.is_file():
        # Single file specified with --batch flag
        image_files = [input_dir]
        input_dir = input_dir.parent
    else:
        # Directory specified
        image_files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    if not image_files:
        click.echo("No image files found in directory", err=True)
        sys.exit(1)

    # Set up output directory
    if not output_dir:
        output_dir = input_dir / "withoutbg-results"

    output_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        click.echo(f"Found {len(image_files)} images")
        click.echo(f"Output directory: {output_dir}")

    # Process images
    with click.progressbar(image_files, label="Processing images") as bar:
        for image_file in bar:
            try:
                # Generate output path
                output_path = output_dir / f"{image_file.stem}-withoutbg.{format}"

                # Remove background
                result = remove_background(image_file, api_key=api_key, model_name=model)

                # Save result
                save_kwargs: dict[str, Any] = {}
                if format.lower() == "jpg":
                    if result.mode == "RGBA":
                        background = Image.new("RGB", result.size, (255, 255, 255))
                        background.paste(result, mask=result.split()[-1])
                        result = background
                    save_kwargs["quality"] = quality
                    save_kwargs["optimize"] = True
                elif format.lower() == "webp":
                    save_kwargs["quality"] = quality
                    save_kwargs["method"] = 6

                # Map format names to PIL format strings
                pil_format = {
                    "jpg": "JPEG",
                    "jpeg": "JPEG",
                    "png": "PNG",
                    "webp": "WEBP",
                }
                result.save(
                    output_path,
                    format=pil_format.get(format.lower(), format.upper()),
                    **save_kwargs,
                )

            except Exception as e:
                if verbose:
                    click.echo(f"\n❌ Failed to process {image_file}: {e}", err=True)
                continue


if __name__ == "__main__":
    main()
