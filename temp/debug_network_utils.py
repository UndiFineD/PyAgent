
import logging
import sys
import os

# Set up logging to stdout
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s: %(message)s')

# Adjust path to find the module
sys.path.append(os.getcwd())

print("Importing network_utils...")
try:
    from src.infrastructure.swarm.network.network_utils import get_local_network_ip
    print("Import successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

print("Calling get_local_network_ip()...")
try:
    ip = get_local_network_ip()
    print(f"Result: {ip}")
except Exception as e:
    print(f"Function call failed: {e}")
    import traceback
    traceback.print_exc()
