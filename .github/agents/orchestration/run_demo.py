import sys
# We selectively import backend explicitly from the file path to avoid sys.path pollution
import importlib.util
backend_spec = importlib.util.spec_from_file_location("backend", ".github/agents/code/backend.py")
backend_module = importlib.util.module_from_spec(backend_spec)
sys.modules["backend"] = backend_module
backend_spec.loader.exec_module(backend_module)

import deploy_global_infra
deploy_global_infra.simulate_global_deployment_intent()
