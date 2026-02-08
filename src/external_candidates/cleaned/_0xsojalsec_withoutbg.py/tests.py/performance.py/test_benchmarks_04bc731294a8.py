# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\tests\performance\test_benchmarks.py
"""Performance benchmarks for withoutbg processing."""

import gc
import time
from unittest.mock import Mock, patch

import numpy as np
import pytest
from PIL import Image
from withoutbg.core import remove_background, remove_background_batch
from withoutbg.models import SnapModel


@pytest.fixture
def benchmark_images():
    """Create test images of various sizes for benchmarking."""
    sizes = [
        (256, 256),  # Small
        (512, 512),  # Medium
        (1024, 768),  # Large
        (2048, 1536),  # XL
    ]

    images = {}
    for size in sizes:
        name = f"{size[0]}x{size[1]}"
        images[name] = Image.new("RGB", size, color=(128, 64, 192))

    return images


@pytest.fixture
def mock_onnx_setup():
    """Setup mocked ONNX environment for performance testing."""
    with patch("withoutbg.models.ort.InferenceSession") as mock_session:
        with patch("pathlib.Path.exists", return_value=True):
            # Mock sessions with realistic behavior
            sessions = []
            for _ in range(3):
                session = Mock()
                depth_output = np.random.rand(1, 518, 518).astype(np.float32)
                session.run.return_value = [depth_output]
                sessions.append(session)

            mock_session.side_effect = sessions
            yield sessions


class TestProcessingBenchmarks:
    """Benchmark processing performance."""

    def test_small_image_processing_time(self, benchmark_images, mock_onnx_setup):
        """Benchmark processing time for small images."""
        image = benchmark_images["256x256"]

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (256, 256), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Measure processing time
                start_time = time.time()
                result = remove_background(image)
                end_time = time.time()

                processing_time = end_time - start_time

                # Assertions
                assert isinstance(result, Image.Image)
                assert processing_time < 5.0  # Should complete within 5 seconds

                # Print benchmark result
                print(f"Small image (256x256) processing time: {processing_time:.3f}s")

    def test_medium_image_processing_time(self, benchmark_images, mock_onnx_setup):
        """Benchmark processing time for medium images."""
        image = benchmark_images["512x512"]

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (512, 512), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Measure processing time
                start_time = time.time()
                result = remove_background(image)
                end_time = time.time()

                processing_time = end_time - start_time

                # Assertions
                assert isinstance(result, Image.Image)
                assert processing_time < 10.0  # Should complete within 10 seconds

                print(f"Medium image (512x512) processing time: {processing_time:.3f}s")

    def test_large_image_processing_time(self, benchmark_images, mock_onnx_setup):
        """Benchmark processing time for large images."""
        image = benchmark_images["1024x768"]

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (1024, 768), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Measure processing time
                start_time = time.time()
                result = remove_background(image)
                end_time = time.time()

                processing_time = end_time - start_time

                # Assertions
                assert isinstance(result, Image.Image)
                assert processing_time < 20.0  # Should complete within 20 seconds

                print(f"Large image (1024x768) processing time: {processing_time:.3f}s")

    def test_xl_image_processing_time(self, benchmark_images, mock_onnx_setup):
        """Benchmark processing time for extra large images."""
        image = benchmark_images["2048x1536"]

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (2048, 1536), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Measure processing time
                start_time = time.time()
                result = remove_background(image)
                end_time = time.time()

                processing_time = end_time - start_time

                # Assertions
                assert isinstance(result, Image.Image)
                assert processing_time < 30.0  # Should complete within 30 seconds

                print(f"XL image (2048x1536) processing time: {processing_time:.3f}s")

    def test_batch_processing_throughput(self, mock_onnx_setup):
        """Benchmark batch processing throughput."""
        # Create multiple test images
        test_images = []
        for i in range(10):
            image = Image.new("RGB", (512, 384), color=(i * 25, i * 20, i * 15))
            test_images.append(image)

        with patch("withoutbg.core.remove_background") as mock_remove_bg:
            # Mock individual processing
            mock_results = []
            for image in test_images:
                mock_result = Image.new("RGBA", image.size, color=(100, 150, 200, 128))
                mock_results.append(mock_result)

            mock_remove_bg.side_effect = mock_results

            # Measure batch processing time
            start_time = time.time()
            results = remove_background_batch(test_images)
            end_time = time.time()

            total_time = end_time - start_time
            throughput = len(test_images) / total_time

            # Assertions
            assert len(results) == len(test_images)
            assert throughput > 1.0  # Should process at least 1 image per second

            print(f"Batch processing throughput: {throughput:.2f} images/second")

    def test_model_initialization_time(self):
        """Benchmark model initialization time."""
        with patch("withoutbg.models.ort.InferenceSession") as mock_session:
            with patch("pathlib.Path.exists", return_value=True):
                mock_session.return_value = Mock()

                # Measure initialization time
                start_time = time.time()
                model = SnapModel()
                end_time = time.time()

                init_time = end_time - start_time

                # Assertions
                assert model is not None
                assert init_time < 5.0  # Should initialize within 5 seconds

                print(f"Model initialization time: {init_time:.3f}s")

    def test_preprocessing_performance(self, benchmark_images, mock_onnx_setup):
        """Benchmark preprocessing performance."""
        image = benchmark_images["1024x768"]
        model = SnapModel()

        # Measure preprocessing time
        start_time = time.time()
        preprocessed = model._preprocess_for_depth(image, 518, 518, 14)
        end_time = time.time()

        preprocessing_time = end_time - start_time

        # Assertions
        assert isinstance(preprocessed, np.ndarray)
        assert preprocessing_time < 1.0  # Should preprocess within 1 second

        print(f"Preprocessing time (1024x768): {preprocessing_time:.3f}s")

    def test_depth_estimation_performance(self, benchmark_images, mock_onnx_setup):
        """Benchmark depth estimation performance."""
        image = benchmark_images["512x512"]
        model = SnapModel()

        # Measure depth estimation time
        start_time = time.time()
        depth_map = model._estimate_depth(image)
        end_time = time.time()

        depth_time = end_time - start_time

        # Assertions
        assert isinstance(depth_map, Image.Image)
        assert depth_time < 2.0  # Should complete within 2 seconds

        print(f"Depth estimation time (512x512): {depth_time:.3f}s")

    def test_concurrent_processing_performance(self, mock_onnx_setup):
        """Benchmark concurrent processing simulation."""
        # Create test images
        test_images = [Image.new("RGB", (256, 256), color=(i * 50, i * 30, i * 20)) for i in range(5)]

        processing_times = []

        for image in test_images:
            with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                    mock_alpha = Image.new("L", (256, 256), color=128)
                    mock_matting.return_value = mock_alpha
                    mock_refiner.return_value = mock_alpha

                    # Measure individual processing time
                    start_time = time.time()
                    result = remove_background(image)
                    end_time = time.time()

                    processing_times.append(end_time - start_time)
                    assert isinstance(result, Image.Image)

        avg_time = sum(processing_times) / len(processing_times)
        max_time = max(processing_times)
        min_time = min(processing_times)

        # Assertions
        assert avg_time < 5.0  # Average should be under 5 seconds
        assert max_time < 10.0  # No single processing should exceed 10 seconds

        print(f"Concurrent processing - Avg: {avg_time:.3f}s, Min: {min_time:.3f}s, Max: {max_time:.3f}s")

    def test_api_response_time_simulation(self):
        """Benchmark simulated API response time."""
        test_image = Image.new("RGB", (512, 384), color=(128, 64, 192))

        with patch("requests.Session.post") as mock_post:
            # Simulate API response with delay
            mock_response = Mock()
            mock_response.ok = True
            mock_response.status_code = 200

            # Create mock response image
            import base64
            import io

            buffer = io.BytesIO()
            result_image = Image.new("RGBA", test_image.size, color=(128, 64, 192, 128))
            result_image.save(buffer, format="PNG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            mock_response.json.return_value = {"image": image_b64}

            # Add artificial delay to simulate network
            def delayed_response(*args, **kwargs):
                time.sleep(0.1)  # 100ms simulated network delay
                return mock_response

            mock_post.side_effect = delayed_response

            # Measure API processing time
            start_time = time.time()
            result = remove_background(test_image, api_key="sk_test_key")
            end_time = time.time()

            api_time = end_time - start_time

            # Assertions
            assert isinstance(result, Image.Image)
            assert api_time >= 0.1  # Should include our simulated delay
            assert api_time < 5.0  # Should complete within 5 seconds total

            print(f"Simulated API processing time: {api_time:.3f}s")


class TestScalabilityBenchmarks:
    """Test scalability and resource usage."""

    def test_memory_scaling_with_image_size(self, mock_onnx_setup):
        """Test memory usage scaling with image size."""
        sizes = [(256, 256), (512, 512), (1024, 768), (1536, 1024)]

        for size in sizes:
            # Force garbage collection before test
            gc.collect()

            test_image = Image.new("RGB", size, color=(100, 150, 200))

            with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                    mock_alpha = Image.new("L", size, color=128)
                    mock_matting.return_value = mock_alpha
                    mock_refiner.return_value = mock_alpha

                    # Process image
                    result = remove_background(test_image)

                    # Verify processing completed
                    assert isinstance(result, Image.Image)
                    assert result.size == size

                    print(f"Successfully processed {size[0]}x{size[1]} image")

                    # Clean up
                    del result
                    del test_image
                    gc.collect()

    def test_batch_size_scaling(self, mock_onnx_setup):
        """Test performance scaling with batch size."""
        batch_sizes = [1, 5, 10, 20]

        for batch_size in batch_sizes:
            # Create batch of test images
            test_images = [Image.new("RGB", (256, 256), color=(i * 10, i * 15, i * 20)) for i in range(batch_size)]

            with patch("withoutbg.core.remove_background") as mock_remove_bg:
                # Mock individual processing
                mock_results = []
                for image in test_images:
                    mock_result = Image.new("RGBA", image.size, color=(100, 150, 200, 128))
                    mock_results.append(mock_result)

                mock_remove_bg.side_effect = mock_results

                # Measure batch processing time
                start_time = time.time()
                results = remove_background_batch(test_images)
                end_time = time.time()

                batch_time = end_time - start_time
                time_per_image = batch_time / batch_size

                # Assertions
                assert len(results) == batch_size
                assert time_per_image < 5.0  # Should average under 5 seconds per image

                print(f"Batch size {batch_size}: {batch_time:.3f}s total, {time_per_image:.3f}s per image")

                # Clean up
                del results
                del test_images
                gc.collect()

    def test_repeated_processing_stability(self, mock_onnx_setup):
        """Test performance stability over repeated processing."""
        test_image = Image.new("RGB", (512, 384), color=(128, 64, 192))
        processing_times = []

        # Process same image multiple times
        for _i in range(10):
            with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                    mock_alpha = Image.new("L", (512, 384), color=128)
                    mock_matting.return_value = mock_alpha
                    mock_refiner.return_value = mock_alpha

                    start_time = time.time()
                    result = remove_background(test_image)
                    end_time = time.time()

                    processing_times.append(end_time - start_time)
                    assert isinstance(result, Image.Image)

                    # Clean up
                    del result
                    gc.collect()

        # Analyze stability
        avg_time = sum(processing_times) / len(processing_times)
        max_time = max(processing_times)
        min_time = min(processing_times)
        variance = sum((t - avg_time) ** 2 for t in processing_times) / len(processing_times)

        # Assertions for stability
        assert variance < 1.0  # Low variance indicates stable performance
        assert max_time / min_time < 3.0  # Max shouldn't be more than 3x min

        print(f"Repeated processing - Avg: {avg_time:.3f}s, Variance: {variance:.6f}")


@pytest.mark.performance
class TestRegressionBenchmarks:
    """Performance regression tests to catch performance degradation."""

    def test_baseline_performance_regression(self, mock_onnx_setup):
        """Test against baseline performance to catch regressions."""
        test_image = Image.new("RGB", (512, 512), color=(128, 64, 192))

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (512, 512), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Measure processing time
                start_time = time.time()
                result = remove_background(test_image)
                end_time = time.time()

                processing_time = end_time - start_time

                # Baseline performance thresholds (adjust based on expected performance)
                BASELINE_512x512_TIME = 10.0  # seconds

                # Assertions
                assert isinstance(result, Image.Image)
                assert processing_time < BASELINE_512x512_TIME, (
                    f"Performance regression detected: {processing_time:.3f}s > {BASELINE_512x512_TIME}s"
                )

                print(f"Baseline test (512x512): {processing_time:.3f}s (threshold: {BASELINE_512x512_TIME}s)")
