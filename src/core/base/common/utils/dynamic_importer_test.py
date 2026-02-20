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

try:
    import importlib
except ImportError:
    import importlib



try:
    from core.base.common.utils.dynamic_importer import (
except ImportError:
    from core.base.common.utils.dynamic_importer import (

    PlaceholderModule,
    LazyModuleRegistry,
    LazyAttribute,
    import_from_path,
    resolve_obj_by_qualname,
    resolve_obj_by_qualname_parts,
    lazy_import,
    safe_import,
    register_lazy_module,
    get_lazy_module,
    reload_module,
    unload_module,
    is_module_available,
    get_module_version,
    require_module,
)


def test_dynamic_importer_symbols_basic():
    # Basic sanity checks: the exported symbols exist and behave predictably
    assert PlaceholderModule is not None
    assert LazyModuleRegistry is not None
    assert LazyAttribute is not None

    assert callable(import_from_path)
    assert callable(resolve_obj_by_qualname)
    assert callable(resolve_obj_by_qualname_parts)
    assert callable(lazy_import)
    assert callable(safe_import)
    assert callable(register_lazy_module)
    assert callable(get_lazy_module)
    assert callable(reload_module)
    assert callable(unload_module)
    assert callable(is_module_available)
    assert callable(get_module_version)
    assert callable(require_module)

