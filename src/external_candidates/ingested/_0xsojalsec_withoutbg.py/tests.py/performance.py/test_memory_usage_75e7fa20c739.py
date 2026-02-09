# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-withoutbg\tests\performance\test_memory_usage.py
"""Memory usage tests for withoutbg processing."""

import gc
import os
import sys
import tempfile
from unittest.mock import Mock, patch

import numpy as np
import pytest
from PIL import Image
from withoutbg.core import remove_background, remove_background_batch
from withoutbg.models import SnapModel


def get_memory_usage():
    """Get current memory usage in MB (approximate)."""
    # This is a simplified memory check - in real scenarios you might use psutil
    gc.collect()
    return sys.getsizeof(gc.get_objects()) / (1024 * 1024)


@pytest.fixture
def mock_onnx_setup():
    """Setup mocked ONNX environment for memory testing."""
    with patch("withoutbg.models.ort.InferenceSession") as mock_session:
        with patch("pathlib.Path.exists", return_value=True):
            # Mock sessions
            sessions = []
            for _ in range(3):
                session = Mock()
                depth_output = np.random.rand(1, 518, 518).astype(np.float32)
                session.run.return_value = [depth_output]
                sessions.append(session)

            mock_session.side_effect = sessions
            yield sessions


class TestMemoryUsage:
    """Test memory usage patterns."""

    def test_single_image_memory_usage(self, mock_onnx_setup):
        """Test memory usage for single image processing."""
        # Force garbage collection
        gc.collect()
        initial_memory = get_memory_usage()

        test_image = Image.new("RGB", (1024, 768), color=(128, 64, 192))

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (1024, 768), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Process image
                result = remove_background(test_image)

                # Check memory during processing
                peak_memory = get_memory_usage()
                memory_increase = peak_memory - initial_memory

                # Assertions
                assert isinstance(result, Image.Image)
                assert (
                    memory_increase < 500
                )  # Should not increase memory by more than 500MB

                print(f"Single image memory increase: {memory_increase:.2f}MB")

                # Clean up
                del result
                del test_image
                gc.collect()

                # Check memory after cleanup
                final_memory = get_memory_usage()
                memory_after_cleanup = final_memory - initial_memory

                # Memory should be mostly cleaned up
                assert memory_after_cleanup < memory_increase / 2

    def test_large_image_memory_usage(self, mock_onnx_setup):
        """Test memory usage with large images."""
        gc.collect()
        initial_memory = get_memory_usage()

        # Create large image
        large_image = Image.new("RGB", (2048, 1536), color=(100, 150, 200))

        with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
            with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                mock_alpha = Image.new("L", (2048, 1536), color=128)
                mock_matting.return_value = mock_alpha
                mock_refiner.return_value = mock_alpha

                # Process large image
                result = remove_background(large_image)

                peak_memory = get_memory_usage()
                memory_increase = peak_memory - initial_memory

                # Assertions
                assert isinstance(result, Image.Image)
                assert result.size == (2048, 1536)

                # Large images should still be manageable
                assert memory_increase < 1000  # Should not exceed 1GB increase

                print(
                    f"Large image (2048x1536) memory increase: {memory_increase:.2f}MB"
                )

                # Clean up
                del result
                del large_image
                gc.collect()

    def test_batch_processing_memory_usage(self, mock_onnx_setup):
        """Test memory usage during batch processing."""
        gc.collect()
        initial_memory = get_memory_usage()

        # Create batch of images
        batch_size = 10
        test_images = [
            Image.new("RGB", (512, 384), color=(i * 25, i * 20, i * 15))
            for i in range(batch_size)
        ]

        with patch("withoutbg.core.remove_background") as mock_remove_bg:
            # Mock individual processing
            mock_results = []
            for image in test_images:
                mock_result = Image.new("RGBA", image.size, color=(100, 150, 200, 128))
                mock_results.append(mock_result)

            mock_remove_bg.side_effect = mock_results

            # Process batch
            results = remove_background_batch(test_images)

            peak_memory = get_memory_usage()
            memory_increase = peak_memory - initial_memory

            # Assertions
            assert len(results) == batch_size

            # Memory usage should scale reasonably with batch size
            expected_max_memory = batch_size * 50  # Rough estimate: 50MB per image
            assert memory_increase < expected_max_memory

            print(
                f"Batch processing ({batch_size} images) memory increase: "
                f"{memory_increase:.2f}MB"
            )

            # Clean up
            del results
            del test_images
            gc.collect()

    def test_sequential_processing_memory_accumulation(self, mock_onnx_setup):
        """Test that sequential processing doesn't accumulate memory."""
        gc.collect()
        initial_memory = get_memory_usage()

        memory_readings = [initial_memory]

        # Process multiple images sequentially
        for i in range(5):
            test_image = Image.new("RGB", (512, 384), color=(i * 50, i * 30, i * 20))

            with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                    mock_alpha = Image.new("L", (512, 384), color=128)
                    mock_matting.return_value = mock_alpha
                    mock_refiner.return_value = mock_alpha

                    # Process image
                    result = remove_background(test_image)

                    # Clean up immediately
                    del result
                    del test_image
                    gc.collect()

                    # Record memory
                    current_memory = get_memory_usage()
                    memory_readings.append(current_memory)

        # Check memory accumulation
        final_memory = memory_readings[-1]
        memory_growth = final_memory - initial_memory

        # Should not accumulate significant memory
        assert memory_growth < 100  # Should not grow by more than 100MB

        print(f"Sequential processing memory growth: {memory_growth:.2f}MB")

        # Check that memory didn't continuously increase
        max_memory = max(memory_readings)
        memory_variance = max_memory - min(memory_readings)
        assert memory_variance < 200  # Reasonable variance

    def test_model_initialization_memory_usage(self):
        """Test memory usage during model initialization."""
        gc.collect()
        initial_memory = get_memory_usage()

        with patch("withoutbg.models.ort.InferenceSession") as mock_session:
            with patch("pathlib.Path.exists", return_value=True):
                mock_session.return_value = Mock()

                # Initialize model
                model = SnapModel()

                post_init_memory = get_memory_usage()
                memory_increase = post_init_memory - initial_memory

                # Assertions
                assert model is not None
                assert (
                    memory_increase < 100
                )  # Model init should not use excessive memory

                print(f"Model initialization memory increase: {memory_increase:.2f}MB")

                # Clean up
                del model
                gc.collect()

    def test_preprocessing_memory_efficiency(self, mock_onnx_setup):
        """Test memory efficiency of preprocessing operations."""
        gc.collect()
        initial_memory = get_memory_usage()

        test_image = Image.new("RGB", (1024, 768), color=(128, 64, 192))
        model = SnapModel()

        # Test preprocessing
        preprocessed = model._preprocess_for_depth(test_image, 518, 518, 14)

        post_preprocess_memory = get_memory_usage()
        memory_increase = post_preprocess_memory - initial_memory

        # Assertions
        assert isinstance(preprocessed, np.ndarray)
        assert memory_increase < 50  # Preprocessing should be memory efficient

        print(f"Preprocessing memory increase: {memory_increase:.2f}MB")

        # Clean up
        del preprocessed
        del test_image
        del model
        gc.collect()

    def test_memory_leak_detection(self, mock_onnx_setup):
        """Test for potential memory leaks in repeated processing."""
        gc.collect()
        initial_memory = get_memory_usage()

        # Process the same image multiple times
        for _iteration in range(10):
            test_image = Image.new("RGB", (256, 256), color=(100, 150, 200))

            with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                with patch("withoutbg.models.SnapModel._refiner_stage") as mock_refiner:
                    mock_alpha = Image.new("L", (256, 256), color=128)
                    mock_matting.return_value = mock_alpha
                    mock_refiner.return_value = mock_alpha

                    # Process image
                    result = remove_background(test_image)

                    # Immediately clean up
                    del result
                    del test_image
                    gc.collect()

        final_memory = get_memory_usage()
        memory_growth = final_memory - initial_memory

        # Should not leak significant memory
        assert (
            memory_growth < 50
        )  # Should not grow by more than 50MB after 10 iterations

        print(f"Memory leak test - Growth after 10 iterations: {memory_growth:.2f}MB")

    def test_numpy_array_memory_management(self, mock_onnx_setup):
        """Test memory management of numpy arrays in processing."""
        gc.collect()
        initial_memory = get_memory_usage()

        test_image = Image.new("RGB", (512, 512), color=(128, 64, 192))

        # Convert to numpy array and back
        image_array = np.array(test_image)
        processed_array = image_array.copy()
        processed_array[:, :, 0] = 255  # Modify array

        result_image = Image.fromarray(processed_array)

        post_processing_memory = get_memory_usage()
        memory_increase = post_processing_memory - initial_memory

        # Clean up arrays
        del image_array
        del processed_array
        del result_image
        del test_image
        gc.collect()

        final_memory = get_memory_usage()
        memory_after_cleanup = final_memory - initial_memory

        # Assertions
        assert memory_increase < 100  # Array operations should be reasonable
        assert memory_after_cleanup < memory_increase / 2  # Should clean up well

        print(
            f"Numpy array memory - Peak: {memory_increase:.2f}MB, "
            f"After cleanup: {memory_after_cleanup:.2f}MB"
        )

    def test_image_format_memory_usage(self, mock_onnx_setup):
        """Test memory usage with different image formats."""
        formats_memory = {}

        # Test different image formats
        formats = ["RGB", "RGBA", "L"]
        sizes = [(512, 512), (1024, 768)]

        for fmt in formats:
            for size in sizes:
                gc.collect()
                initial_memory = get_memory_usage()

                # Create image in specific format
                if fmt == "RGB":
                    test_image = Image.new(fmt, size, color=(128, 64, 192))
                elif fmt == "RGBA":
                    test_image = Image.new(fmt, size, color=(128, 64, 192, 200))
                elif fmt == "L":
                    test_image = Image.new(fmt, size, color=128)

                # Convert to array and back (simulate processing)
                array = np.array(test_image)
                result_image = Image.fromarray(array)

                peak_memory = get_memory_usage()
                memory_increase = peak_memory - initial_memory

                key = f"{fmt}_{size[0]}x{size[1]}"
                formats_memory[key] = memory_increase

                # Clean up
                del test_image
                del array
                del result_image
                gc.collect()

        # Print results
        for key, memory in formats_memory.items():
            print(f"Format {key} memory usage: {memory:.2f}MB")

        # Basic assertions
        for memory in formats_memory.values():
            assert memory < 200  # No format should use excessive memory

    def test_temporary_file_memory_usage(self, mock_onnx_setup):
        """Test memory usage when processing temporary files."""
        gc.collect()
        initial_memory = get_memory_usage()

        # Create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            test_image = Image.new("RGB", (512, 384), color=(100, 150, 200))
            test_image.save(tmp_file.name, "JPEG")

            try:
                with patch("withoutbg.models.SnapModel._matting_stage") as mock_matting:
                    with patch(
                        "withoutbg.models.SnapModel._refiner_stage"
                    ) as mock_refiner:
                        mock_alpha = Image.new("L", (512, 384), color=128)
                        mock_matting.return_value = mock_alpha
                        mock_refiner.return_value = mock_alpha

                        # Process file
                        result = remove_background(tmp_file.name)

                        peak_memory = get_memory_usage()
                        memory_increase = peak_memory - initial_memory

                        # Assertions
                        assert isinstance(result, Image.Image)
                        assert (
                            memory_increase < 100
                        )  # File processing should be efficient

                        print(
                            f"Temporary file processing memory increase: "
                            f"{memory_increase:.2f}MB"
                        )

                        # Clean up
                        del result
                        gc.collect()

            finally:
                os.unlink(tmp_file.name)
