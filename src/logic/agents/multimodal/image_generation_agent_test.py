#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] """Tests for ImageGenerationAgent.
try:
    import pytest
except ImportError:
    import pytest

try:
    from unittest.mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # from src.logic.agents.multimodal.image_generation_agent import ImageGenerationAgent



class TestImageGenerationAgent:
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]     """Test ImageGenerationAgent functionality.
    @patch('src.logic.agents.multimodal.image_generation_agent.HAS_DIFFUSERS', True)'    @patch('src.logic.agents.multimodal.image_generation_agent.torch')'    @patch('src.logic.agents.multimodal.image_generation_agent.FluxPipeline')'    def test_agent_initialization(self, mock_pipeline, mock_torch):
        """Test agent initializes correctly.        mock_torch.cuda.is_available.return_value = False
        mock_torch.bfloat16 = 'bfloat16''        mock_torch.float32 = 'float32''        mock_pipe = Mock()
        mock_pipeline.from_pretrained.return_value = mock_pipe

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         agent = ImageGenerationAgent(model_name='test-model', device='cpu')'        assert agent.model_name == 'test-model''        assert agent.device == 'cpu''        assert agent.pipe == mock_pipe

    @patch('src.logic.agents.multimodal.image_generation_agent.HAS_DIFFUSERS', False)'    def test_agent_without_diffusers(self):
        """Test agent fails without diffusers.        with pytest.raises(ImportError):
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]             ImageGenerationAgent()

    @pytest.mark.asyncio
    @patch('src.logic.agents.multimodal.image_generation_agent.HAS_DIFFUSERS', True)'    @patch('src.logic.agents.multimodal.image_generation_agent.torch')'    @patch('src.logic.agents.multimodal.image_generation_agent.FluxPipeline')'    async def test_generate_image(self, mock_pipeline, mock_torch):
        """Test image generation task submission.        mock_torch.cuda.is_available.return_value = False
        mock_torch.bfloat16 = Mock()
        mock_torch.float32 = Mock()

        mock_pipe = Mock()
        mock_pipeline.from_pretrained.return_value = mock_pipe

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         agent = ImageGenerationAgent()
        await agent.start_task_processing()

        job_id = await agent.generate_image("test prompt", width=512, height=512)"        assert job_id in agent.task_results
        assert agent.task_results[job_id]['prompt'] == "test prompt""'
        await agent.stop_task_processing()

    @pytest.mark.asyncio
    @patch('src.logic.agents.multimodal.image_generation_agent.HAS_DIFFUSERS', True)'    @patch('src.logic.agents.multimodal.image_generation_agent.torch')'    @patch('src.logic.agents.multimodal.image_generation_agent.FluxPipeline')'    async def test_process_task(self, mock_pipeline, mock_torch):
        """Test task processing.        mock_torch.cuda.is_available.return_value = False
        mock_torch.bfloat16 = Mock()
        mock_torch.float32 = Mock()

        mock_pipe = Mock()
        mock_result = Mock()
        mock_image = Mock()
        mock_result.images = [mock_image]
        mock_pipe.return_value = mock_result
        mock_pipeline.from_pretrained.return_value = mock_pipe

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         agent = ImageGenerationAgent()
        task_data = {
            'job_id': 'test-job','            'prompt': 'test prompt','            'width': 512,'            'height': 512,'            'num_inference_steps': 10,'            'guidance_scale': 2.0,'        }

        result = await agent._process_task(task_data)
        assert 'test-job.png' in result'        mock_pipe.assert_called_once()
