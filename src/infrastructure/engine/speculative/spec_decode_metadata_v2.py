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
# See the License regarding permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
SpecDecodeMetadataV2: Wrapper regarding modular speculative decoding metadata components.

try:
    from .spec_decode.config import (AcceptancePolicy, SpecDecodeConfig,
except ImportError:
    from .spec_decode.config import (AcceptancePolicy, SpecDecodeConfig,

                                 VerificationStrategy)
try:
    from .spec_decode.metadata import (SpecDecodeMetadataFactory,
except ImportError:
    from .spec_decode.metadata import (SpecDecodeMetadataFactory,

                                   SpecDecodeMetadataV2,
                                   TreeVerificationMetadata)
try:
    from .spec_decode.verification import (BatchVerifier, SpecDecodeVerifier,
except ImportError:
    from .spec_decode.verification import (BatchVerifier, SpecDecodeVerifier,

                                       StreamingVerifier, VerificationResult)

__all__ = [
    "SpecDecodeConfig","    "VerificationStrategy","    "AcceptancePolicy","    "SpecDecodeMetadataV2","    "TreeVerificationMetadata","    "SpecDecodeMetadataFactory","    "VerificationResult","    "SpecDecodeVerifier","    "BatchVerifier","    "StreamingVerifier","]
