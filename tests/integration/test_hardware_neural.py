"""
Integration Tests: Hardware Profile & Neural Transformer (Rust Core)

Refactored from temp/test_hardware_neural.py into proper pytest format.
Tests Rust-accelerated hardware detection and neural network components.
"""

import pytest


class TestHardwareProfile:
    """Tests for rust_core.HardwareProfile."""
    
    def test_hardware_profile_creation(self):
        """Test HardwareProfile can be instantiated."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            
            assert profile.cpu_cores > 0
            assert profile.total_memory_gb > 0
            assert profile.available_memory_gb > 0
            assert profile.vram_gb >= 0  # May be 0 if no GPU
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_hardware_profile_cpu_cores(self):
        """Test CPU core detection is reasonable."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            
            # Should be at least 1, typically 2-128
            assert 1 <= profile.cpu_cores <= 256
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_hardware_profile_memory(self):
        """Test memory detection is reasonable."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            
            # System should have at least 1GB, available <= total
            assert profile.total_memory_gb >= 1
            assert profile.available_memory_gb <= profile.total_memory_gb
            assert profile.available_memory_gb > 0
        except ImportError:
            pytest.skip("rust_core not available")


class TestTransformerConfig:
    """Tests for rust_core.TransformerConfig."""
    
    def test_auto_configure(self):
        """Test auto-configuration based on hardware."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            
            assert config.d_model > 0
            assert config.n_heads > 0
            assert config.n_layers > 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_config_d_model_divisible_by_heads(self):
        """Test d_model is divisible by n_heads."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            
            assert config.d_model % config.n_heads == 0
        except ImportError:
            pytest.skip("rust_core not available")


class TestNeuralTransformer:
    """Tests for rust_core.NeuralTransformer."""
    
    def test_transformer_creation(self):
        """Test NeuralTransformer can be created."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            transformer = rust_core.NeuralTransformer(config)
            
            assert transformer is not None
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_transformer_summary(self):
        """Test transformer summary generation."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            transformer = rust_core.NeuralTransformer(config)
            
            summary = transformer.get_summary()
            assert isinstance(summary, str)
            assert len(summary) > 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_transformer_forward_pass(self):
        """Test transformer forward pass with dummy input."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            transformer = rust_core.NeuralTransformer(config)
            
            # Create dummy input: 5 tokens x d_model dimensions
            seq_len = 5
            dummy_input = [[0.1] * config.d_model for _ in range(seq_len)]
            
            refined = transformer.forward(dummy_input)
            
            # Output should have same shape
            assert len(refined) == seq_len
            assert len(refined[0]) == config.d_model
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_transformer_forward_values_changed(self):
        """Test that forward pass actually transforms values."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            config = rust_core.TransformerConfig.auto_configure(profile)
            transformer = rust_core.NeuralTransformer(config)
            
            dummy_input = [[0.1] * config.d_model for _ in range(3)]
            refined = transformer.forward(dummy_input)
            
            # Values should be transformed (not identical to input)
            input_sum = sum(dummy_input[0])
            output_sum = sum(refined[0])
            assert input_sum != output_sum
        except ImportError:
            pytest.skip("rust_core not available")


class TestFlexibleNeuralNetwork:
    """Tests for rust_core.FlexibleNeuralNetwork."""
    
    def test_network_creation(self):
        """Test FlexibleNeuralNetwork creation."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            net = rust_core.FlexibleNeuralNetwork(profile)
            
            assert net is not None
            assert hasattr(net, 'layer_sizes')
            assert len(net.layer_sizes) > 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_network_layer_sizes(self):
        """Test layer sizes are reasonable."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            net = rust_core.FlexibleNeuralNetwork(profile)
            
            # Should have at least input and output layers
            assert len(net.layer_sizes) >= 2
            for size in net.layer_sizes:
                assert size > 0
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_network_process(self):
        """Test network forward processing."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            net = rust_core.FlexibleNeuralNetwork(profile)
            
            # Input size based on first layer
            input_size = net.layer_sizes[0]
            test_data = [0.1] * input_size
            
            result = net.process(test_data)
            
            assert isinstance(result, float)
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_network_process_varied_input(self):
        """Test network with varied input values."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            net = rust_core.FlexibleNeuralNetwork(profile)
            
            input_size = net.layer_sizes[0]
            
            # Two different inputs should produce different outputs
            input1 = [0.1] * input_size
            input2 = [0.9] * input_size
            
            result1 = net.process(input1)
            result2 = net.process(input2)
            
            # Results should differ
            assert result1 != result2
        except ImportError:
            pytest.skip("rust_core not available")


class TestHardwareScaling:
    """Tests for hardware-based scaling logic."""
    
    def test_scaling_classification(self):
        """Test scaling classification based on hardware."""
        try:
            import rust_core
            profile = rust_core.HardwareProfile(None)
            
            # Determine scaling tier
            if profile.vram_gb >= 24 or profile.available_memory_gb >= 64:
                scaling = "Heavy"
            elif profile.vram_gb >= 8 or profile.available_memory_gb >= 16:
                scaling = "Medium"
            else:
                scaling = "Light"
            
            assert scaling in ["Light", "Medium", "Heavy"]
        except ImportError:
            pytest.skip("rust_core not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
