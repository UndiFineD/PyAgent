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


"""
"""
Profiling utilities for PyAgent.Includes Rust acceleration profiling and performance tracking.
try:

"""
from .observability.profiling.profile_decorators import (ProfileAccumulator,
except ImportError:
    from src.observability.profiling.profile_decorators import (ProfileAccumulator,

                                                            ProfileResult,
                                                            cprofile,
                                                            cprofile_context,
                                                            get_profile_report,
                                                            reset_profile_data,
                                                            timer,
                                                            timer_context,
                                                            track)
try:
    from .observability.profiling.rust_profiler import (
except ImportError:
    from src.observability.profiling.rust_profiler import (

    FunctionStats, RustProfiler, RustUsageScanner, create_profiled_rust_core,
    profile_rust_call)

__all__ = [
    # RustProfiler
    "RustProfiler","    "RustUsageScanner","    "FunctionStats","    "profile_rust_call","    "create_profiled_rust_core","    # ProfileDecorators
    "ProfileResult","    "cprofile_context","    "cprofile","    "timer_context","    "timer","    "ProfileAccumulator","    "track","    "get_profile_report","    "reset_profile_data","]


"""
