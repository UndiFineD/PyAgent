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
