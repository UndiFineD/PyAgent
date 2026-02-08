# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\examples\basic_usage.py
#!/usr/bin/env python3
"""Basic usage examples for withoutbg."""

import withoutbg
from PIL import Image


def basic_local_processing():
    """Example: Basic background removal with local Snap model."""
    print("🟢 Example: Local processing with Snap model")

    # Remove background using local model (free)
    result = withoutbg.remove_background("input.jpg")
    result.save("output_snap.png")

    print("✅ Background removed and saved as output_snap.png")
    print("🎯 Want best quality? Try withoutbg.com")


def api_processing():
    """Example: Background removal with Studio API."""
    print("\n🔴 Example: Cloud processing with Studio API")

    # Set your API key (get one at withoutbg.com)
    API_KEY = "sk_your_api_key_here"

    try:
        # Remove background using Studio API (best quality)
        result = withoutbg.remove_background("input.jpg", api_key=API_KEY)
        result.save("output_studio.png")

        print("✅ Background removed with Studio API")
        print("🎯 Best quality processing")

    except withoutbg.APIError as e:
        print(f"❌ API Error: {e}")
        print("💡 Get your API key at https://withoutbg.com")


def batch_processing():
    """Example: Process multiple images at once."""
    print("\n📦 Example: Batch processing")

    # List of images to process
    image_files = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]

    # Process all images and save to directory
    results = withoutbg.remove_background_batch(image_files, output_dir="batch_results/")

    print(f"✅ Processed {len(results)} images")
    print("📁 Results saved in batch_results/ directory")


def e_commerce_example():
    """Example: E-commerce product photos."""
    print("\n🛍️ Example: E-commerce product processing")

    from pathlib import Path

    # Process entire product catalog
    product_dir = Path("products/")
    if product_dir.exists():
        product_images = list(product_dir.glob("*.jpg"))

        # Use API for best quality in production
        results = withoutbg.remove_background_batch(
            product_images,
            output_dir="catalog-withoutbg/",
            api_key="sk_your_key",  # Replace with your key
        )

        print(f"✅ Processed {len(results)} product images")
    else:
        print("📁 Create a 'products/' directory with images to try this example")


def custom_background_example():
    """Example: Add custom background after removal."""
    print("\n🎨 Example: Custom background replacement")

    # Remove background
    foreground = withoutbg.remove_background("portrait.jpg")

    # Load custom background
    background = Image.open("gradient_background.jpg")

    # Resize background to match foreground
    background = background.resize(foreground.size, Image.Resampling.LANCZOS)

    # Composite the images
    if foreground.mode == "RGBA":
        background.paste(foreground, (0, 0), foreground)  # Use alpha as mask
    else:
        background.paste(foreground, (0, 0))

    background.save("custom_background_result.jpg")
    print("✅ Custom background applied and saved")


def quality_comparison():
    """Example: Compare different model tiers."""
    print("\n🏆 Example: Quality comparison")

    input_image = "test_image.jpg"

    # Snap model (local, free)
    print("Processing with Snap model...")
    snap_result = withoutbg.remove_background(input_image)
    snap_result.save("comparison_snap.png")

    # Studio model (API, best quality)
    print("Processing with Studio API...")
    try:
        studio_result = withoutbg.remove_background(input_image, api_key="sk_your_key")
        studio_result.save("comparison_studio.png")

        print("✅ Comparison complete!")
        print("📊 Compare results:")
        print("   - comparison_snap.png (Snap model)")
        print("   - comparison_studio.png (Studio API)")

    except withoutbg.APIError:
        print("⚠️  Studio API requires valid API key")


if __name__ == "__main__":
    print("🎭 withoutbg Examples")
    print("=" * 50)

    # Run examples (comment out as needed)
    basic_local_processing()
    # api_processing()  # Uncomment and add your API key
    # batch_processing()
    # e_commerce_example()
    # custom_background_example()
    # quality_comparison()

    print("\n🎯 Get best quality results at https://withoutbg.com")
