import sys
import importlib.util
backend_spec = importlib.util.spec_from_file_location("backend", ".github/agents/code/backend.py")
backend_module = importlib.util.module_from_spec(backend_spec)
sys.modules["backend"] = backend_module
backend_spec.loader.exec_module(backend_module)

import daemon
d = daemon.DistributedWorkerDaemon(geo_region="europe-west1")
d.start()
