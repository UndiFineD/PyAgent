import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path.cwd()))

try:
    print("Attempting to import MultimodalCore...")
    from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
    print("Success!")
    
    print("Attempting to import AuthCore...")
    from src.core.base.common.auth_core import AuthCore
    print("Success!")
    
    print("Attempting to import RegistryCore...")
    from src.core.base.common.registry_core import RegistryCore
    print("Success!")
    
    print("Attempting to import TemplateCore...")
    from src.core.base.common.template_core import TemplateCore
    print("Success!")
    
    print("Attempting to import ObservabilityCore...")
    from src.observability.stats.observability_core import ObservabilityCore
    print("Success!")
    
    # Test MultimodalStreamSession with a dummy hook
    core = MultimodalCore()
    # Enable Hardware:NPU channel
    core.active_channels["Hardware"] = "NPU"
    session = MultimodalStreamSession(core)
    # The session clones active_channels, but we should make sure Hardware is copied
    session.channels["Hardware"] = "NPU"
    
    def my_mod(frags):
        for f in frags:
            if f["type"] == "text" and "trigger" in f["content"]:
                f["content"] = f["content"].replace("trigger", "<Hardware:NPU_INIT>")
        return frags
        
    session.add_modificator(my_mod)
    raw = "Hello trigger world"
    # We want to see the fragments before filtering too
    fragments = core.parse_stream(raw) # Initial
    fragments = session._reparse_if_needed(my_mod(fragments))
    print(f"Intermediate fragments: {fragments}")
    
    filtered = session.filter_response(raw)
    print(f"Final filtered result: {filtered}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
