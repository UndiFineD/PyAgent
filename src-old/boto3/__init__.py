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

r"""Lightweight boto3 shim used by tests when the real library is not required.

This module provides a very small subset of the :mod:`boto3` API that is sufficient
for tests and legacy modules which expect to be able to do::

    import boto3
    client = boto3.client("s3")

The returned client is a dummy object that does not talk to AWS. Any attempt to
call an unsupported method on the dummy client will raise :class:`NotImplementedError`
with a clear error message so that tests fail loudly rather than silently.
"""

from __future__ import annotations

from typing import Any, Callable


class DummyBoto3Client:
    """Minimal stand-in for a real boto3 client.

    The dummy client is intentionally lightweight. It records the service name and any
    keyword configuration passed at construction time but does not implement any real
    AWS operations.

    Attribute access uses :meth:`__getattr__` to create stub callables on demand. Any
    such callables will raise :class:`NotImplementedError` when invoked, making it
    obvious in tests if an unexpected method is used.
    """

    def __init__(self, service_name: str, **kwargs: Any) -> None:
        self._service_name = service_name
        self._config = dict(kwargs) if kwargs else {}

    @property
    def service_name(self) -> str:
        """Return the logical name of the AWS service for this client."""

        return self._service_name

    @property
    def config(self) -> dict[str, Any]:
        """Return any configuration values supplied at construction time."""

        return dict(self._config)

    def __repr__(self) -> str:
        return f"<DummyBoto3Client service_name={self._service_name!r}>"

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Dynamically provide stub methods for any attribute access.

        This mirrors the dynamic nature of real boto3 clients without needing to know
        the full API surface. Accessing an unknown attribute will return a callable
        that, when invoked, raises :class:`NotImplementedError`.
        """

        def _missing(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"DummyBoto3Client for service {self._service_name!r} "
                f"does not implement method {name!r}."
            )

        return _missing


def client(service_name: str, **kwargs: Any) -> DummyBoto3Client:
    """Return a dummy boto3 client for the specified service.

    Parameters
    ----------
    service_name:
        Name of the AWS service for which a client is requested (for example,
        ``\"s3\"`` or ``\"ec2\"``). The value is stored on the dummy client for
        introspection in tests but does not affect behavior.
    **kwargs:
        Optional configuration keyword arguments. These are stored on the client and
        can be inspected by tests if necessary, but they do not change behavior.
    """

    return DummyBoto3Client(service_name, **kwargs)
