from src.core.base.managers.PluginManager import PluginManager
from pathlib import Path

pm = PluginManager()
discovered = pm.discover()
print(f"Discovered: {discovered}")

if "test_sandbox" in pm.loaded_meta:
    meta = pm.loaded_meta["test_sandbox"]
    print(f"Meta for test_sandbox: {meta}")
    
    plugin = pm.load_plugin("test_sandbox")
    if plugin:
        print("Plugin loaded successfully.")
        # Try to run it on a 'src' file (should be blocked if read:src is missing)
        res = plugin.run(Path("src/core/base/BaseAgent.py"), {})
        print(f"Run result on src: {res}")
        
        # Try to run it on a 'temp' file (should be allowed)
        res = plugin.run(Path("temp/test.txt"), {})
        print(f"Run result on temp: {res}")
else:
    print("test_sandbox not discovered.")
