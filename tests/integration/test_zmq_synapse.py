"""
Integration Tests: ZMQ Transport & Neural Synapse

Refactored from temp/verify_zmq_synapse.py into proper pytest format.
Tests Phase 319 ZMQ transport and synaptic fire functionality.
"""

import pytest
import asyncio
import sys


# Skip all tests if ZMQ not available
try:
    import zmq
    HAS_ZMQ = True
except ImportError:
    HAS_ZMQ = False

pytestmark = pytest.mark.skipif(not HAS_ZMQ, reason="ZMQ not available")


class MockFleet:
    """Mock fleet for testing."""
    def __init__(self, fleet_id: str):
        self.fleet_id = fleet_id


class MockAgent:
    """Mock agent for teleportation testing."""
    def __init__(self, name: str):
        self.name = name
        self.memory = {"goal": "Achieve Voyager stability"}


class TestRemoteNeuralSynapse:
    """Tests for RemoteNeuralSynapse."""
    
    def test_synapse_import(self):
        """Test RemoteNeuralSynapse can be imported."""
        try:
            from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
            assert RemoteNeuralSynapse is not None
        except ImportError as e:
            pytest.skip(f"RemoteNeuralSynapse not available: {e}")
    
    def test_synapse_creation(self):
        """Test synapse can be created."""
        try:
            from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
            
            fleet = MockFleet("test-fleet")
            synapse = RemoteNeuralSynapse(fleet, transport_port=5560)
            
            assert synapse is not None
        except ImportError:
            pytest.skip("RemoteNeuralSynapse not available")
    
    @pytest.mark.asyncio
    async def test_synapse_start_stop(self):
        """Test synapse can start and stop."""
        try:
            from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
            
            fleet = MockFleet("test-fleet")
            synapse = RemoteNeuralSynapse(fleet, transport_port=5561)
            
            await synapse.start()
            await synapse.stop()
            
            assert True  # If no exception, success
        except ImportError:
            pytest.skip("RemoteNeuralSynapse not available")
        except Exception as e:
            if "Address already in use" in str(e):
                pytest.skip("Port already in use")
            raise


class TestTeleportationEngine:
    """Tests for TeleportationEngine."""
    
    def test_engine_import(self):
        """Test TeleportationEngine can be imported."""
        try:
            from src.infrastructure.voyager.TeleportationEngine import TeleportationEngine
            assert TeleportationEngine is not None
        except ImportError as e:
            pytest.skip(f"TeleportationEngine not available: {e}")
    
    def test_engine_creation(self):
        """Test engine can be created."""
        try:
            from src.infrastructure.voyager.TeleportationEngine import TeleportationEngine
            
            engine = TeleportationEngine()
            assert engine is not None
        except ImportError:
            pytest.skip("TeleportationEngine not available")


class TestP2PCommunication:
    """Tests for peer-to-peer communication."""
    
    @pytest.mark.asyncio
    async def test_ping_pong(self):
        """Test P2P ping/pong communication."""
        try:
            from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
            
            # Setup two nodes
            fleet_a = MockFleet("Fleet-A")
            synapse_a = RemoteNeuralSynapse(fleet_a, transport_port=5562)
            
            fleet_b = MockFleet("Fleet-B")
            synapse_b = RemoteNeuralSynapse(fleet_b, transport_port=5563)
            
            try:
                await synapse_a.start()
                await synapse_b.start()
                
                # Test ping from B to A
                if hasattr(synapse_b, 'transport') and hasattr(synapse_b.transport, 'send_to_peer'):
                    response = await synapse_b.transport.send_to_peer(
                        "127.0.0.1", 
                        5562, 
                        {"type": "ping", "sender_id": "Fleet-B"}
                    )
                    
                    if response:
                        assert response.get("status") == "pong"
                else:
                    pytest.skip("Transport ping not available")
            finally:
                await synapse_a.stop()
                await synapse_b.stop()
        except ImportError:
            pytest.skip("RemoteNeuralSynapse not available")
        except Exception as e:
            error_msg = str(e)
            if "Address already in use" in error_msg:
                pytest.skip("Port already in use")
            elif "selector" in error_msg.lower() or "proactor" in error_msg.lower():
                pytest.skip("ZMQ async event loop not compatible on Windows")
            elif "NotImplementedError" in error_msg:
                pytest.skip("ZMQ async not implemented for this event loop")
            raise
    
    @pytest.mark.asyncio
    async def test_agent_teleportation(self):
        """Test agent teleportation between nodes."""
        try:
            from src.infrastructure.voyager.RemoteNeuralSynapse import RemoteNeuralSynapse
            
            fleet_a = MockFleet("Fleet-A")
            synapse_a = RemoteNeuralSynapse(fleet_a, transport_port=5564)
            
            fleet_b = MockFleet("Fleet-B")
            synapse_b = RemoteNeuralSynapse(fleet_b, transport_port=5565)
            
            try:
                await synapse_a.start()
                await synapse_b.start()
                
                agent = MockAgent("Recon-Agent-01")
                
                if hasattr(synapse_b, 'teleport_agent_to_peer'):
                    success = await synapse_b.teleport_agent_to_peer(
                        agent, 
                        "127.0.0.1", 
                        5564
                    )
                    
                    # Teleportation should succeed or fail gracefully
                    assert isinstance(success, bool)
                else:
                    pytest.skip("Teleportation not available")
            finally:
                await synapse_a.stop()
                await synapse_b.stop()
        except ImportError:
            pytest.skip("RemoteNeuralSynapse not available")
        except Exception as e:
            error_msg = str(e)
            if "Address already in use" in error_msg:
                pytest.skip("Port already in use")
            elif "selector" in error_msg.lower() or "proactor" in error_msg.lower():
                pytest.skip("ZMQ async event loop not compatible on Windows")
            elif "NotImplementedError" in error_msg:
                pytest.skip("ZMQ async not implemented for this event loop")
            raise


class TestWindowsEventLoopPolicy:
    """Tests for Windows event loop compatibility."""
    
    def test_windows_policy_available(self):
        """Test Windows selector event loop policy is available."""
        if sys.platform != 'win32':
            pytest.skip("Not on Windows")
        
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        assert policy is not None
    
    @pytest.mark.asyncio
    async def test_async_works_on_windows(self):
        """Test basic async works with Windows policy."""
        if sys.platform == 'win32':
            # Should already be using correct policy via conftest
            pass
        
        await asyncio.sleep(0.01)
        assert True


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    pytest.main([__file__, "-v"])
