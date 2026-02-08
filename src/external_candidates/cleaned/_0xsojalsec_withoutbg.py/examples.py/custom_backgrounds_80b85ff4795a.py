# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\examples\custom_backgrounds.py
#!/usr/bin/env python3
"""Custom background replacement examples."""

from pathlib import Path

import numpy as np
import withoutbg
from PIL import Image, ImageDraw, ImageFilter


def solid_color_background():
    """Replace background with solid color."""
    print("🎨 Example: Solid color background")

    # Remove original background
    foreground = withoutbg.remove_background("portrait.jpg")

    # Create solid color backgrounds
    colors = [
        (255, 255, 255),  # White
        (0, 0, 0),  # Black
        (70, 130, 180),  # Steel Blue
        (255, 182, 193),  # Light Pink
        (144, 238, 144),  # Light Green
    ]

    for i, color in enumerate(colors):
        # Create background
        background = Image.new("RGB", foreground.size, color)

        # Composite
        if foreground.mode == "RGBA":
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))

        # Save
        color_name = ["white", "black", "blue", "pink", "green"][i]
        background.save(f"portrait_{color_name}_bg.jpg", quality=95)

    print("✅ Solid color backgrounds created")


def gradient_background():
    """Create gradient backgrounds."""
    print("\n🌈 Example: Gradient backgrounds")

    foreground = withoutbg.remove_background("portrait.jpg")
    width, height = foreground.size

    # Create different gradients
    gradients = [
        # Vertical blue to purple
        {"start": (0, 100, 255), "end": (128, 0, 255), "direction": "vertical"},
        # Horizontal orange to pink
        {"start": (255, 165, 0), "end": (255, 20, 147), "direction": "horizontal"},
        # Diagonal green to blue
        {"start": (0, 255, 127), "end": (0, 191, 255), "direction": "diagonal"},
    ]

    for i, grad in enumerate(gradients):
        # Create gradient
        background = create_gradient(width, height, grad["start"], grad["end"], grad["direction"])

        # Composite
        if foreground.mode == "RGBA":
            background.paste(foreground, (0, 0), foreground)
        else:
            background.paste(foreground, (0, 0))

        # Save
        background.save(f"portrait_gradient_{i + 1}.jpg", quality=95)

    print("✅ Gradient backgrounds created")


def create_gradient(width, height, start_color, end_color, direction):
    """Create a gradient image."""
    background = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(background)

    if direction == "vertical":
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

    elif direction == "horizontal":
        for x in range(width):
            ratio = x / width
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return background


def scenic_background():
    """Replace with scenic/nature backgrounds."""
    print("\n🏞️ Example: Scenic backgrounds")

    foreground = withoutbg.remove_background("portrait.jpg")

    # List of scenic backgrounds (you'd have these images)
    scenic_files = [
        "beach_sunset.jpg",
        "mountain_landscape.jpg",
        "city_skyline.jpg",
        "forest_path.jpg",
    ]

    for scenic_file in scenic_files:
        if Path(scenic_file).exists():
            # Load scenic background
            scenic_bg = Image.open(scenic_file)

            # Resize to match foreground
            scenic_bg = scenic_bg.resize(foreground.size, Image.Resampling.LANCZOS)

            # Optional: Blur background slightly for depth effect
            scenic_bg = scenic_bg.filter(ImageFilter.GaussianBlur(radius=1.5))

            # Composite
            if foreground.mode == "RGBA":
                scenic_bg.paste(foreground, (0, 0), foreground)
            else:
                scenic_bg.paste(foreground, (0, 0))

            # Save
            output_name = f"portrait_{Path(scenic_file).stem}.jpg"
            scenic_bg.save(output_name, quality=95)

            print(f"✅ Created {output_name}")
        else:
            print(f"⚠️  Scenic background not found: {scenic_file}")


def professional_studio_background():
    """Create professional studio-style backgrounds."""
    print("\n📸 Example: Professional studio backgrounds")

    foreground = withoutbg.remove_background("portrait.jpg")
    width, height = foreground.size

    # Studio background 1: Soft gray with vignette
    studio_bg1 = Image.new("RGB", (width, height), (240, 240, 240))

    # Add subtle vignette effect
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Create radial gradient for vignette
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2

    for radius in range(max_radius, 0, -5):
        opacity = int(255 * (1 - radius / max_radius) * 0.3)
        draw.ellipse(
            [
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
            ],
            fill=opacity,
        )

    # Apply vignette
    vignette = Image.new("RGB", (width, height), (200, 200, 200))
    studio_bg1 = Image.composite(vignette, studio_bg1, mask)

    # Composite with foreground
    if foreground.mode == "RGBA":
        studio_bg1.paste(foreground, (0, 0), foreground)

    studio_bg1.save("portrait_studio_gray.jpg", quality=95)

    # Studio background 2: Classic white with shadow
    studio_bg2 = Image.new("RGB", (width, height), (255, 255, 255))

    # Add subtle shadow effect
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    # Create drop shadow (simplified)
    if foreground.mode == "RGBA":
        # Create shadow from alpha channel
        alpha = foreground.split()[-1]
        shadow_offset = 5
        shadow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_img.paste((50, 50, 50, 100), (shadow_offset, shadow_offset), alpha)
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=3))

        # Composite shadow, then foreground
        studio_bg2 = Image.alpha_composite(studio_bg2.convert("RGBA"), shadow_img).convert("RGB")
        studio_bg2.paste(foreground, (0, 0), foreground)
    else:
        studio_bg2.paste(foreground, (0, 0))

    studio_bg2.save("portrait_studio_white.jpg", quality=95)

    print("✅ Professional studio backgrounds created")


def social_media_templates():
    """Create social media ready images with backgrounds."""
    print("\n📱 Example: Social media templates")

    foreground = withoutbg.remove_background("portrait.jpg")

    # Instagram square format
    instagram_size = (1080, 1080)
    instagram_bg = Image.new("RGB", instagram_size, (255, 182, 193))  # Light pink

    # Center the foreground
    fg_ratio = min(800 / foreground.width, 800 / foreground.height)
    new_fg_size = (int(foreground.width * fg_ratio), int(foreground.height * fg_ratio))
    foreground_resized = foreground.resize(new_fg_size, Image.Resampling.LANCZOS)

    paste_x = (instagram_size[0] - new_fg_size[0]) // 2
    paste_y = (instagram_size[1] - new_fg_size[1]) // 2

    if foreground_resized.mode == "RGBA":
        instagram_bg.paste(foreground_resized, (paste_x, paste_y), foreground_resized)
    else:
        instagram_bg.paste(foreground_resized, (paste_x, paste_y))

    instagram_bg.save("portrait_instagram.jpg", quality=95)

    # LinkedIn banner format
    linkedin_size = (1584, 396)
    linkedin_bg = Image.new("RGB", linkedin_size, (0, 119, 181))  # LinkedIn blue

    # Position portrait on left side
    fg_ratio = min(350 / foreground.width, 350 / foreground.height)
    new_fg_size = (int(foreground.width * fg_ratio), int(foreground.height * fg_ratio))
    foreground_resized = foreground.resize(new_fg_size, Image.Resampling.LANCZOS)

    paste_x = 50
    paste_y = (linkedin_size[1] - new_fg_size[1]) // 2

    if foreground_resized.mode == "RGBA":
        linkedin_bg.paste(foreground_resized, (paste_x, paste_y), foreground_resized)
    else:
        linkedin_bg.paste(foreground_resized, (paste_x, paste_y))

    linkedin_bg.save("portrait_linkedin_banner.jpg", quality=95)

    print("✅ Social media templates created")
    print("   - portrait_instagram.jpg (1080x1080)")
    print("   - portrait_linkedin_banner.jpg (1584x396)")


if __name__ == "__main__":
    print("🎨 Custom Background Examples")
    print("=" * 50)

    # Check if input image exists
    if not Path("portrait.jpg").exists():
        print("❌ Please add a 'portrait.jpg' image to try these examples")
        print("💡 Any portrait photo will work!")
        exit(1)

    try:
        # Run all examples
        solid_color_background()
        gradient_background()
        scenic_background()
        professional_studio_background()
        social_media_templates()

        print("\n✅ All background examples complete!")
        print("🎯 Perfect for:")
        print("   - E-commerce product photos")
        print("   - Professional headshots")
        print("   - Social media content")
        print("   - Marketing materials")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have a 'portrait.jpg' file in this directory")

    print("\n🎯 Get best quality processing at https://withoutbg.com")
