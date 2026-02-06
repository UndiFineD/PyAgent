# Extracted from: C:\DEV\PyAgent\.external\skills\skills\luruibu\beauty-generation-api\scripts\quick_generate_test.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick random generation test script - optimized for 5-second generation validation
Tests random beauty generation with immediate download and notification
"""

import json
import os
import sys
import time

from generate import BeautyAPIClient, _default_out_dir


def test_quick_generation():
    """Test quick random generation with immediate download and notification."""

    # Configuration
    API_BASE = "https://gen1.diversityfaces.org"
    API_KEY = os.environ.get(
        "BEAUTY_API_KEY", "ak_OymjErKQRs-brINJuHFxKwIbxbZHq2KRiEzYthnwxMI"
    )

    print("🚀 Starting quick generation test...")
    print(f"📡 API: {API_BASE}")
    print("=" * 60)

    # Initialize client with optimized settings
    client = BeautyAPIClient(API_BASE, API_KEY)
    client.timeout = 15  # Short timeout for quick test

    # Prepare output directory
    out_dir = _default_out_dir()
    os.makedirs(out_dir, exist_ok=True)

    # Test parameters - use random generation for variety
    test_params = {"width": 1024, "height": 1024, "seed": -1}  # Random seed for variety

    print("📝 Using random generation for variety")
    print("🎲 Parameters will be randomly selected by the API")
    print()

    # Start generation
    total_start = time.time()

    try:
        print("🎨 Submitting random generation request...")
        result = client.generate_random(**test_params)  # Use random generation instead

        if not result.get("success"):
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            return False

        prompt_id = result["prompt_id"]
        print(f"✅ Request submitted (ID: {prompt_id[:8]}...)")
        print(f"📝 Generated prompt: {result.get('prompt', 'N/A')}")
        print()

        # Wait for completion with optimized polling
        print("⏳ Waiting for completion...")
        final_status = client.wait_for_completion(prompt_id, 60)  # 1 minute max

        generation_time = time.time() - total_start

        # Download images immediately
        download_start = time.time()
        downloaded_files = []

        for i, img in enumerate(final_status["images"]):
            filename = img["filename"]
            save_name = f"quick-test-{i+1}.webp"
            save_path = os.path.join(out_dir, save_name)

            client.download_image(
                filename,
                save_path,
                format="webp",
                subfolder=img.get("subfolder", ""),
                type=img.get("type", "output"),
            )

            downloaded_files.append(
                {
                    "file": save_name,
                    "path": os.path.abspath(save_path),
                    "size": os.path.getsize(save_path),
                }
            )

        download_time = time.time() - download_start
        total_time = time.time() - total_start

        # Success notification
        print("\n" + "=" * 80)
        print("🎉 QUICK GENERATION TEST SUCCESSFUL!")
        print(f"⏱️  Total time: {total_time:.1f}s")
        print(f"🎨 Generation time: {generation_time:.1f}s")
        print(f"📥 Download time: {download_time:.1f}s")
        print("=" * 80)

        print("\n📸 Generated files:")
        for file_info in downloaded_files:
            size_mb = file_info["size"] / (1024 * 1024)
            print(f"  • {file_info['file']} ({size_mb:.1f}MB)")
            print(f"    📍 {file_info['path']}")

        print(f"\n📂 Output directory: {out_dir}")
        print("💡 Images are ready for immediate viewing!")

        # Save test results
        test_results = {
            "timestamp": time.time(),
            "total_time": total_time,
            "generation_time": generation_time,
            "download_time": download_time,
            "files": downloaded_files,
            "generation_type": "random",
            "params": test_params,
            "generated_prompt": result.get("prompt", ""),
            "random_params_used": result.get("random_params", {}),
            "success": True,
        }

        results_path = os.path.join(out_dir, "quick_test_results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)

        print(f"📊 Test results saved: {results_path}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main test function."""
    print("Quick Random Generation Test - Beauty API")
    print("Optimized for 5-second generation validation with random parameters")
    print("=" * 60)

    success = test_quick_generation()

    if success:
        print("\n✅ Quick generation test completed successfully!")
        return 0
    else:
        print("\n❌ Quick generation test failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
