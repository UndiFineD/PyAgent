# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\examples\e_commerce_batch.py
#!/usr/bin/env python3
"""E-commerce batch processing example."""

import json
import time
from pathlib import Path

import withoutbg
from PIL import Image


def process_product_catalog():
    """Process an entire product catalog for e-commerce."""
    print("🛍️ E-commerce Product Catalog Processing")
    print("=" * 50)

    # Configuration
    input_dir = Path("product_catalog")
    output_dir = Path("catalog-withoutbg")
    api_key = "sk_your_api_key_here"  # Replace with your key

    # Create directories if they don't exist
    output_dir.mkdir(exist_ok=True)

    # Find all product images
    image_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    product_images = []

    for ext in image_extensions:
        product_images.extend(input_dir.glob(f"*{ext}"))
        product_images.extend(input_dir.glob(f"*{ext.upper()}"))

    if not product_images:
        print(f"❌ No images found in {input_dir}")
        print("💡 Create the directory and add some product photos to try this example")
        return

    print(f"📦 Found {len(product_images)} product images")

    # Process with timing
    start_time = time.time()

    try:
        # Option 1: Use API for best quality (recommended for production)
        print("🔴 Processing with Studio API (best quality)...")
        results = withoutbg.remove_background_batch(product_images, output_dir=output_dir, api_key=api_key)

        processing_method = "Studio API"

    except withoutbg.APIError as e:
        print(f"⚠️  API Error: {e}")
        print("🟢 Falling back to local Snap model...")

        # Option 2: Fallback to local processing
        results = withoutbg.remove_background_batch(product_images, output_dir=output_dir)

        processing_method = "Local Snap"

    end_time = time.time()
    total_time = end_time - start_time

    # Generate report
    print("\n📊 Processing Report")
    print("-" * 30)
    print(f"Images processed: {len(results)}")
    print(f"Processing method: {processing_method}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average per image: {total_time / len(results):.2f} seconds")
    print(f"Output directory: {output_dir}")

    # Save processing report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "images_processed": len(results),
        "processing_method": processing_method,
        "total_time_seconds": round(total_time, 2),
        "average_time_per_image": round(total_time / len(results), 2),
        "input_directory": str(input_dir),
        "output_directory": str(output_dir),
    }

    with open(output_dir / "processing_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"📄 Report saved: {output_dir}/processing_report.json")


def optimize_for_web():
    """Optimize processed images for web use."""
    print("\n🌐 Web Optimization")
    print("-" * 30)

    output_dir = Path("catalog-withoutbg")
    web_dir = Path("catalog_web")
    web_dir.mkdir(exist_ok=True)

    # Find processed images
    processed_images = list(output_dir.glob("*.png"))

    if not processed_images:
        print("❌ No processed images found. Run process_product_catalog() first.")
        return

    print(f"🔧 Optimizing {len(processed_images)} images for web...")

    for img_path in processed_images:
        try:
            # Load image
            img = Image.open(img_path)

            # Create different sizes for responsive design
            sizes = {
                "thumbnail": (150, 150),
                "small": (300, 300),
                "medium": (600, 600),
                "large": (1200, 1200),
            }

            stem = img_path.stem

            for size_name, dimensions in sizes.items():
                # Resize maintaining aspect ratio
                img_copy = img.copy()
                img_copy.thumbnail(dimensions, Image.Resampling.LANCZOS)

                # Save as WebP for better compression
                webp_path = web_dir / f"{stem}_{size_name}.webp"
                img_copy.save(webp_path, "WebP", quality=85, method=6)

                # Also save PNG for compatibility
                png_path = web_dir / f"{stem}_{size_name}.png"
                img_copy.save(png_path, "PNG", optimize=True)

        except Exception as e:
            print(f"⚠️  Failed to process {img_path}: {e}")

    print(f"✅ Web-optimized images saved to {web_dir}")


def generate_html_preview():
    """Generate HTML preview of processed products."""
    print("\n📄 Generating HTML Preview")
    print("-" * 30)

    web_dir = Path("catalog_web")
    thumbnail_images = list(web_dir.glob("*_thumbnail.webp"))

    if not thumbnail_images:
        print("❌ No thumbnail images found. Run optimize_for_web() first.")
        return

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Catalog - Background Removed</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { text-align: center; margin-bottom: 30px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
        .product { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .product img { width: 100%; height: 150px; object-fit: contain; border-radius: 4px; }
        .product h3 { margin: 10px 0 5px 0; font-size: 14px; }
        .badge { display: inline-block; background: #4CAF50; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }
        .footer { text-align: center; margin-top: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛍️ Product Catalog</h1>
        <p>Backgrounds removed with <strong>withoutbg</strong></p>
        <div class="badge">AI-Powered</div>
    </div>
    
    <div class="grid">
"""

    for img_path in sorted(thumbnail_images):
        product_name = img_path.stem.replace("_thumbnail", "").replace("_", " ").title()

        html_content += f"""
        <div class="product">
            <img src="{img_path.name}" alt="{product_name}">
            <h3>{product_name}</h3>
            <div class="badge">No Background</div>
        </div>
"""

    html_content += """
    </div>
    
    <div class="footer">
        <p>Processed with <a href="https://withoutbg.com">withoutbg</a></p>
        <p>🎯 Get best quality results with Studio API</p>
    </div>
</body>
</html>
"""

    html_path = web_dir / "index.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML preview generated: {html_path}")
    print(f"🌐 Open {html_path} in your browser to view the catalog")


if __name__ == "__main__":
    print("🛍️ E-commerce Batch Processing Example")
    print("=" * 50)

    # Step 1: Process product catalog
    process_product_catalog()

    # Step 2: Optimize for web
    optimize_for_web()

    # Step 3: Generate HTML preview
    generate_html_preview()

    print("\n✅ Complete! Your product catalog is ready for e-commerce.")
    print("🎯 Get best quality processing at https://withoutbg.com")
