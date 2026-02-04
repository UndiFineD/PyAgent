#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Integration test for new core services: JobQueue, MultimodalAIService, and TTSService.
"""

import time
import pytest
from src.core.base.logic.job_queue import JobQueue
from src.core.base.logic.multimodal_ai_service import MultimodalAIService, CloudflareProvider, AIServiceConfig
from src.core.base.logic.tts_service import TTSService


class TestNewServicesIntegration:
    """Test integration of the three new core services."""

    def test_job_queue_basic_functionality(self):
        """Test basic job queue operations."""
        queue = JobQueue(max_queue_size=10)
        results = []

        def processor(job_id, data):
            results.append(f"Processed: {data['task']}")
            return f"Result for {data['task']}"

        queue.set_job_processor(processor)
        queue.start()

        # Submit a job
        job_id = queue.submit_job({'task': 'integration_test'})

        # Wait for processing
        time.sleep(0.1)

        # Check status
        status = queue.get_job_status(job_id)
        assert status['status'] == 'completed'
        assert 'Result for integration_test' in status['result']

        queue.stop()

    def test_tts_service_basic_functionality(self):
        """Test TTS service generates audio."""
        tts = TTSService()

        # Generate audio
        audio_data = tts.synthesize("Hello, this is a test.")

        # Should return bytes
        assert isinstance(audio_data, bytes)
        assert len(audio_data) > 0

    def test_multimodal_ai_service_initialization(self):
        """Test multimodal AI service can be initialized and configured."""
        service = MultimodalAIService()

        # Create a mock provider
        config = AIServiceConfig(provider='cloudflare', api_key='test_key')
        provider = CloudflareProvider(config)

        # Register provider
        service.register_provider('cloudflare', provider)

        # Should not raise any exceptions
        assert True

    def test_services_work_together(self):
        """Test that all services can be used together in a workflow."""
        # Initialize all services
        queue = JobQueue(max_queue_size=10)
        tts = TTSService()
        multimodal = MultimodalAIService()

        # Configure multimodal service
        config = AIServiceConfig(provider='cloudflare', api_key='test_key')
        provider = CloudflareProvider(config)
        multimodal.register_provider('cloudflare', provider)

        # Create a workflow that uses TTS to generate audio for a job
        def workflow_processor(job_id, data):
            text = data.get('text', 'Default message')
            audio = tts.synthesize(text)
            return {
                'text': text,
                'audio_length': len(audio),
                'processed_by': 'integration_test'
            }

        queue.set_job_processor(workflow_processor)
        queue.start()

        # Submit workflow job
        job_id = queue.submit_job({'text': 'Integration test message'})

        # Wait for completion
        time.sleep(0.2)

        # Verify results
        status = queue.get_job_status(job_id)
        assert status['status'] == 'completed'
        result = status['result']
        assert result['text'] == 'Integration test message'
        assert result['audio_length'] > 0
        assert result['processed_by'] == 'integration_test'

        queue.stop()


if __name__ == "__main__":
    # Run the tests
    test_instance = TestNewServicesIntegration()

    print("Running integration tests...")

    try:
        test_instance.test_job_queue_basic_functionality()
        print("✓ JobQueue test passed")
    except Exception as e:
        print(f"✗ JobQueue test failed: {e}")

    try:
        test_instance.test_tts_service_basic_functionality()
        print("✓ TTSService test passed")
    except Exception as e:
        print(f"✗ TTSService test failed: {e}")

    try:
        test_instance.test_multimodal_ai_service_initialization()
        print("✓ MultimodalAIService test passed")
    except Exception as e:
        print(f"✗ MultimodalAIService test failed: {e}")

    try:
        test_instance.test_services_work_together()
        print("✓ Integration workflow test passed")
    except Exception as e:
        print(f"✗ Integration workflow test failed: {e}")

    print("Integration tests completed!")