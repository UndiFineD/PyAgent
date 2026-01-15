from pathlib import Path
import re




def fix_infrastructure_conftest():
    target = Path("tests/unit/infrastructure/conftest.py")
    if not target.exists(): return

    content = target.read_text("utf-8")

    # We want to replace the body of agent_backend_module fixture
    # But it's easier to verify imports first.

    # Check if we need to modify
    if 'submodules =' in content:
        print("Infrastructure conftest already patched.")
        return

    # Replacement block
    old_block = '    with agent_dir_on_path():\n        return load_agent_module("infrastructure/backend/execution_engine.py")'
    new_block = """    with agent_dir_on_path():
        mod = load_agent_module("infrastructure/backend/execution_engine.py")

        # Aggregate classes from other backend modules
        submodules = [
            "AuditLogger", "RequestSigner", "RequestDeduplicator", "VersionNegotiator",
            "CapabilityDiscovery", "RequestRecorder", "ConfigHotReloader", "RequestCompressor",
            "SystemAnalytics", "ConnectionPool", "RequestThrottler", "TTLCache", "ABTester"
        ]






        for sub in submodules:
            try:
                sub_mod = load_agent_module(f"infrastructure/backend/{sub}.py")
                if hasattr(sub_mod, sub):




                    setattr(mod, sub, getattr(sub_mod, sub))
            except Exception as e:
                # Fallback: check if it's already in execution_engine (unlikely given tests)
                pass




        return mod"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        target.write_text(content, "utf-8")




        print("Patched tests/unit/infrastructure/conftest.py")
    else:
        # Retry with simpler match logic or regex if needed, but the strings should match what I saw
        print("Could not match block in infrastructure/conftest.py")






def fix_core_conftest():
    target = Path("tests/unit/core/conftest.py")
    if not target.exists(): return




    content = target.read_text("utf-8")

    if "create_legacy_agent_wrapper" in content:
        print("Core conftest already patched.")
        return

    # Add import
    if "from tests.utils.agent_test_utils" in content:
        content = content.replace("from tests.utils.agent_test_utils", "from tests.utils.legacy_support import create_legacy_agent_wrapper\nfrom tests.utils.agent_test_utils")




    # Patch base_agent_module fixture
    # It currently returns load_agent_module(...)
    # We want to intercept return

    pattern = r'    with agent_dir_on_path\(\):\n        return load_agent_module\("core/base/BaseAgent.py"\)'
    replacement = """    with agent_dir_on_path():
        mod = load_agent_module("core/base/BaseAgent.py")
        if hasattr(mod, "BaseAgent"):
            wrapper = create_legacy_agent_wrapper(mod.BaseAgent)
            mod.BaseAgent = wrapper




            mod.Agent = wrapper
        return mod"""

    con = re.sub(pattern, replacement, content)
    if con != content:
        target.write_text(con, "utf-8")
        print("Patched tests/unit/core/conftest.py")
    else:
        print("Could not match block in core/conftest.py")






if __name__ == "__main__":
    fix_infrastructure_conftest()
    fix_core_conftest()
