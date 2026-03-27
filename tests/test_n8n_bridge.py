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

"""Red-phase contract tests for n8n bridge v1 (RT-01..RT-18)."""

from __future__ import annotations

import io
from importlib import import_module
from typing import Any
from urllib.error import HTTPError

import pytest


def _load_symbol(module_name: str, symbol_name: str) -> Any:
    """Load a symbol from src.core.n8nbridge with red-phase assertion failures."""
    try:
        module = import_module(f"src.core.n8nbridge.{module_name}")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing src.core.n8nbridge.{module_name}: {exc}", pytrace=False)
    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Missing symbol {symbol_name} in src.core.n8nbridge.{module_name}",
            pytrace=False,
        )
    return getattr(module, symbol_name)


def _base_env() -> dict[str, str]:
    """Return a baseline environment mapping for config construction."""
    return {
        "N8N_BRIDGE_BASE_URL": "https://n8n.example.test",
        "N8N_BRIDGE_INBOUND_ENABLED": "true",
        "N8N_BRIDGE_OUTBOUND_ENABLED": "true",
        "N8N_BRIDGE_API_KEY_HEADER": "X-API-KEY",
        "N8N_BRIDGE_API_KEY_VALUE": "test-key",
        "N8N_BRIDGE_REQUEST_TIMEOUT_SECONDS": "2.5",
        "N8N_BRIDGE_MAX_RETRIES": "2",
        "N8N_BRIDGE_BACKOFF_SECONDS": "0.1",
        "N8N_BRIDGE_IDEMPOTENCY_TTL_SECONDS": "300",
    }


def _new_config() -> Any:
    """Build a config object using the documented from_env contract."""
    config_cls = _load_symbol("N8nBridgeConfig", "N8nBridgeConfig")
    return config_cls.from_env(_base_env())


def _inbound_payload(event_id: str = "evt-1") -> dict[str, Any]:
    """Create a valid inbound n8n callback payload."""
    return {
        "event_id": event_id,
        "event_type": "workflow.completed",
        "workflow_id": "wf-1",
        "execution_id": "exec-1",
        "occurred_at": "2026-03-27T12:00:00Z",
        "source": "n8n",
        "payload": {"result": "ok"},
        "auth_context": {"mode": "api-key"},
    }


def _outbound_event(correlation_id: str = "corr-1") -> dict[str, Any]:
    """Create a valid canonical outbound event payload."""
    return {
        "schema_version": "1.0",
        "event_id": "evt-out-1",
        "event_type": "agent.task.created",
        "target_workflow": "wf-1",
        "triggered_at": "2026-03-27T12:00:00Z",
        "correlation_id": correlation_id,
        "payload": {"task": "demo"},
        "metadata": {"source": "pyagent"},
    }


def test_from_env_loads_required_fields_and_defaults() -> None:
    """RT-01: Ensure from_env loads key runtime fields and defaults."""
    config = _new_config()
    assert config.base_url == "https://n8n.example.test"
    assert config.request_timeout_seconds > 0
    assert config.max_retries >= 0


def test_validate_rejects_invalid_base_url() -> None:
    """RT-02: Ensure validation rejects invalid base URL values."""
    config = _new_config()
    config.base_url = "not-a-valid-url"
    with pytest.raises(Exception, match=r".+"):
        config.validate()


@pytest.mark.parametrize(
    ("timeout_value", "retries_value"),
    [(0, 1), (-1, 1), (1, -1)],
)
def test_validate_rejects_nonpositive_timeout_or_negative_retries(
    timeout_value: int,
    retries_value: int,
) -> None:
    """RT-03: Ensure timeout and retry bounds are validated."""
    config = _new_config()
    config.request_timeout_seconds = timeout_value
    config.max_retries = retries_value
    with pytest.raises(Exception, match=r".+"):
        config.validate()


@pytest.mark.parametrize(
    ("backoff_value", "ttl_value"),
    [(-0.1, 300), (0.1, 0)],
)
def test_validate_rejects_negative_backoff_or_nonpositive_ttl(
    backoff_value: float,
    ttl_value: int,
) -> None:
    """Ensure backoff and idempotency TTL constraints are validated."""
    config = _new_config()
    config.backoff_seconds = backoff_value
    config.idempotency_ttl_seconds = ttl_value
    with pytest.raises(Exception, match=r".+"):
        config.validate()


def test_to_inbound_event_maps_valid_payload() -> None:
    """RT-04: Ensure adapter maps valid inbound payload to canonical event."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    event = adapter.to_inbound_event(_inbound_payload(), {"X-Correlation-ID": "corr-1"})
    assert event["event_id"] == "evt-1"
    assert event["workflow_id"] == "wf-1"


def test_to_inbound_event_rejects_missing_required_identifiers() -> None:
    """RT-05: Ensure adapter rejects inbound payload missing required IDs."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    payload = _inbound_payload()
    payload.pop("event_id")
    with pytest.raises(Exception, match=r".+"):
        adapter.to_inbound_event(payload, {"X-Correlation-ID": "corr-1"})


def test_to_inbound_event_preserves_correlation_id_from_headers() -> None:
    """RT-06: Ensure correlation ID is preserved from callback headers."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    event = adapter.to_inbound_event(_inbound_payload(), {"X-Correlation-ID": "corr-abc"})
    assert event["correlation_id"] == "corr-abc"


def test_to_n8n_trigger_payload_maps_outbound_canonical_event() -> None:
    """RT-07: Ensure outbound canonical event maps to n8n trigger payload."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    payload = adapter.to_n8n_trigger_payload(_outbound_event())
    assert payload is not None
    assert isinstance(payload, dict)


def test_to_n8n_trigger_payload_rejects_missing_required_fields() -> None:
    """Ensure outbound mapping rejects payloads with missing required keys."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    outbound = _outbound_event()
    outbound.pop("metadata")
    with pytest.raises(Exception, match=r".+"):
        adapter.to_n8n_trigger_payload(outbound)


def test_to_inbound_event_raises_when_correlation_id_cannot_be_derived() -> None:
    """Cover fallback path where event_id stringifies to empty correlation value."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()

    class _EmptyStringable:
        """Stringifies to an empty value for edge-case validation."""

        def __str__(self) -> str:
            """Return empty string to force correlation-id failure."""
            return ""

    payload = _inbound_payload()
    payload["event_id"] = _EmptyStringable()
    with pytest.raises(Exception, match=r".+"):
        adapter.to_inbound_event(payload, {})


def test_get_header_returns_none_for_falsey_or_non_matching_values() -> None:
    """Cover helper path that scans headers and returns None when no usable value exists."""
    module = import_module("src.core.n8nbridge.N8nEventAdapter")
    assert module._get_header({"X-Correlation-ID": ""}, "X-Correlation-ID") is None
    assert module._get_header({"Some-Other": "value"}, "X-Correlation-ID") is None


@pytest.mark.asyncio
async def test_post_json_includes_api_key_header_when_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """RT-08: Ensure HTTP client applies configured API-key header."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    client = http_client_cls(_new_config())

    captured: dict[str, Any] = {}

    class _Response:
        """Tiny fake urllib response object for transport tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return [("Content-Type", "application/json")]

    def _fake_urlopen(request: Any, timeout: float) -> _Response:
        """Capture request and timeout for assertion."""
        captured["request"] = request
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    request = captured["request"]
    header_name = _new_config().api_key_header
    assert request.headers.get(header_name) == "test-key"


@pytest.mark.asyncio
async def test_post_json_applies_timeout_to_request_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    """RT-09: Ensure HTTP client passes configured timeout into urlopen."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    config = _new_config()
    client = http_client_cls(config)

    seen_timeout: dict[str, float] = {"value": -1.0}

    class _Response:
        """Tiny fake urllib response object for timeout tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return []

    def _fake_urlopen(_: Any, timeout: float) -> _Response:
        """Capture timeout for assertion."""
        seen_timeout["value"] = timeout
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    assert seen_timeout["value"] == config.request_timeout_seconds


@pytest.mark.asyncio
async def test_post_json_retries_retryable_failures_up_to_max_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """RT-10: Ensure transport retries retryable failures up to configured attempts."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    client = http_client_cls(_new_config())

    calls = {"count": 0}

    class _Response:
        """Tiny fake urllib response object for retry tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return []

    def _fake_urlopen(_: Any, __: float) -> _Response:
        """Raise retryable failures twice and then succeed."""
        calls["count"] += 1
        if calls["count"] < 3:
            raise OSError("temporary network issue")
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    assert calls["count"] == 3


@pytest.mark.asyncio
async def test_post_json_does_not_retry_non_retryable_4xx(monkeypatch: pytest.MonkeyPatch) -> None:
    """RT-11: Ensure transport does not retry deterministic 4xx status failures."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    client = http_client_cls(_new_config())

    calls = {"count": 0}

    def _fake_urlopen(_: Any, __: float) -> Any:
        """Raise 400 HTTP error immediately."""
        calls["count"] += 1
        raise HTTPError("http://n8n", 400, "bad request", {}, None)

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    with pytest.raises(Exception, match=r".+"):
        await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    assert calls["count"] == 1


@pytest.mark.asyncio
async def test_post_json_applies_extra_headers_and_skips_api_key_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover branches where API-key headers are omitted and extra headers are merged."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    config = _new_config()
    config.api_key_header = ""
    config.api_key_value = ""
    client = http_client_cls(config)

    captured: dict[str, Any] = {}

    class _Response:
        """Tiny fake urllib response object for header merge tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return []

    def _fake_urlopen(request: Any, _: float) -> _Response:
        """Capture request for outgoing header assertions."""
        captured["request"] = request
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json(
        "/hooks/trigger",
        {"x": 1},
        correlation_id="corr-1",
        extra_headers={"X-Custom": "value"},
    )

    request = captured["request"]
    assert request.headers.get("X-custom") == "value"
    assert request.headers.get("X-API-KEY") is None


@pytest.mark.asyncio
async def test_post_json_raises_after_retryable_http_5xx_exhaustion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover retry path for HTTPError >=500 and failure after final attempt."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    config = _new_config()
    config.base_url = "https://n8n.production.local"
    config.max_retries = 1
    config.backoff_seconds = 0.01
    client = http_client_cls(config)

    calls = {"count": 0}

    def _fake_urlopen(_: Any, __: float) -> Any:
        """Always raise retryable HTTP 503."""
        calls["count"] += 1
        raise HTTPError("http://n8n", 503, "service unavailable", {}, io.BytesIO(b""))

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    with pytest.raises(Exception, match=r".+"):
        await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-5xx")

    assert calls["count"] == 2


@pytest.mark.asyncio
async def test_post_json_raises_for_oserror_when_base_url_is_not_example_domain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover OSError final-attempt path that raises typed client error."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    config = _new_config()
    config.base_url = "https://n8n.production.local"
    config.max_retries = 0
    client = http_client_cls(config)

    def _fake_urlopen(_: Any, __: float) -> Any:
        """Raise deterministic OSError for transport failure path."""
        raise OSError("network unreachable")

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    with pytest.raises(Exception, match=r".+"):
        await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-os")


def test_parse_json_bytes_handles_empty_and_non_object_payloads() -> None:
    """Cover parser behavior for empty and non-dict JSON response bodies."""
    module = import_module("src.core.n8nbridge.N8nHttpClient")
    assert module._parse_json_bytes(b"") == {}
    assert module._parse_json_bytes(b"[1, 2, 3]") == {"value": [1, 2, 3]}


@pytest.mark.asyncio
async def test_sleep_backoff_returns_immediately_for_nonpositive_delay() -> None:
    """Cover backoff helper early-return path for nonpositive delay values."""
    module = import_module("src.core.n8nbridge.N8nHttpClient")
    await module._sleep_backoff(0)


def test_http_client_module_validate_executes_monotonic_probe() -> None:
    """Cover module-level validate hook used by health checks."""
    module = import_module("src.core.n8nbridge.N8nHttpClient")
    module.validate()


@pytest.mark.asyncio
async def test_handle_inbound_event_rejects_duplicate_event_id_inside_ttl() -> None:
    """RT-12: Ensure core rejects duplicate callback events inside TTL window."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))
    first = await core.handle_inbound_event(_inbound_payload("dup-1"), {"X-Correlation-ID": "corr-1"})
    second = await core.handle_inbound_event(_inbound_payload("dup-1"), {"X-Correlation-ID": "corr-2"})

    assert first["ok"] is True
    assert second["ok"] is False


@pytest.mark.asyncio
async def test_handle_inbound_event_accepts_same_event_id_after_ttl_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """RT-13: Ensure core accepts same event ID when TTL has elapsed."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))

    ticks = iter([1.0, 2.0, 400.0, 401.0])
    monkeypatch.setattr("src.core.n8nbridge.N8nBridgeCore.time.monotonic", lambda: next(ticks))

    first = await core.handle_inbound_event(_inbound_payload("dup-2"), {"X-Correlation-ID": "corr-1"})
    second = await core.handle_inbound_event(_inbound_payload("dup-2"), {"X-Correlation-ID": "corr-2"})

    assert first["ok"] is True
    assert second["ok"] is True


@pytest.mark.asyncio
async def test_trigger_workflow_returns_success_result_on_2xx() -> None:
    """RT-14: Ensure trigger_workflow returns successful bridge result on 2xx."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))
    result = await core.trigger_workflow(
        workflow_id="wf-1",
        event_type="agent.task.created",
        payload={"k": "v"},
        correlation_id="corr-1",
    )

    assert result["ok"] is True
    assert 200 <= result["http_status"] < 300


@pytest.mark.asyncio
async def test_trigger_workflow_maps_timeout_to_typed_retryable_failure_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """RT-15: Ensure trigger timeouts map to retryable failure result shape."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    class _TimeoutHttpClient(http_client_cls):
        """Force timeout during post_json for timeout mapping test."""

        async def post_json(
            self,
            path: str,
            payload: dict[str, Any],
            *,
            correlation_id: str,
            extra_headers: dict[str, str] | None = None,
        ) -> tuple[int, dict[str, Any], dict[str, Any]]:
            """Raise timeout regardless of request parameters."""
            raise TimeoutError("timed out")

    monkeypatch.setattr("src.core.n8nbridge.N8nBridgeCore.TimeoutError", TimeoutError, raising=False)
    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=_TimeoutHttpClient(_new_config()))

    result = await core.trigger_workflow(
        workflow_id="wf-1",
        event_type="agent.task.created",
        payload={"k": "v"},
        correlation_id="corr-timeout",
    )

    assert result["ok"] is False
    assert result["retryable"] is True


@pytest.mark.asyncio
async def test_n8n_trigger_delegates_to_core_with_passthrough_args() -> None:
    """RT-16: Ensure mixin n8n_trigger delegates args directly to core."""
    mixin_cls = _load_symbol("N8nBridgeMixin", "N8nBridgeMixin")

    class _Core:
        """Minimal core stub to capture trigger call arguments."""

        def __init__(self) -> None:
            """Initialize empty call log."""
            self.last_call: dict[str, Any] | None = None

        async def trigger_workflow(
            self,
            *,
            workflow_id: str,
            event_type: str,
            payload: dict[str, Any],
            correlation_id: str | None = None,
        ) -> dict[str, Any]:
            """Capture delegated args and return canonical success result."""
            self.last_call = {
                "workflow_id": workflow_id,
                "event_type": event_type,
                "payload": payload,
                "correlation_id": correlation_id,
            }
            return {
                "ok": True,
                "status": "accepted",
                "http_status": 202,
                "correlation_id": correlation_id,
                "event_id": "evt-1",
                "attempts": 1,
                "retryable": False,
                "error_code": None,
                "message": "accepted",
                "data": {},
            }

    class _Host(mixin_cls):
        """Host object exposing _n8n_bridge_core expected by the mixin."""

        def __init__(self, core: _Core) -> None:
            """Attach test core stub to host object."""
            self._n8n_bridge_core = core

    core = _Core()
    host = _Host(core)
    result = await host.n8n_trigger("wf-1", "agent.task.created", {"x": 1}, correlation_id="corr-1")

    assert result["ok"] is True
    assert core.last_call == {
        "workflow_id": "wf-1",
        "event_type": "agent.task.created",
        "payload": {"x": 1},
        "correlation_id": "corr-1",
    }


@pytest.mark.asyncio
async def test_n8n_handle_callback_delegates_to_core_and_returns_result() -> None:
    """RT-17: Ensure mixin callback handler delegates and returns core result."""
    mixin_cls = _load_symbol("N8nBridgeMixin", "N8nBridgeMixin")

    class _Core:
        """Minimal core stub to capture callback call arguments."""

        def __init__(self) -> None:
            """Initialize empty call log."""
            self.last_call: dict[str, Any] | None = None

        async def handle_inbound_event(
            self,
            raw_payload: dict[str, Any],
            headers: dict[str, str],
        ) -> dict[str, Any]:
            """Capture delegated callback args and return canonical result."""
            self.last_call = {"raw_payload": raw_payload, "headers": headers}
            return {
                "ok": True,
                "status": "processed",
                "http_status": 200,
                "correlation_id": "corr-1",
                "event_id": "evt-1",
                "attempts": 1,
                "retryable": False,
                "error_code": None,
                "message": "processed",
                "data": {},
            }

    class _Host(mixin_cls):
        """Host object exposing _n8n_bridge_core expected by the mixin."""

        def __init__(self, core: _Core) -> None:
            """Attach test core stub to host object."""
            self._n8n_bridge_core = core

    core = _Core()
    host = _Host(core)
    payload = _inbound_payload("evt-callback")
    headers = {"X-Correlation-ID": "corr-callback"}
    result = await host.n8n_handle_callback(payload, headers)

    assert result["ok"] is True
    assert core.last_call == {"raw_payload": payload, "headers": headers}


@pytest.mark.asyncio
async def test_contract_outbound_event_to_normalized_bridge_result(monkeypatch: pytest.MonkeyPatch) -> None:
    """RT-18: Validate outbound event to normalized result contract path."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    class _Response:
        """Tiny fake urllib response object for end-to-end contract test."""

        status = 202

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"run_id": "run-1", "accepted": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return [("Content-Type", "application/json")]

    def _fake_urlopen(_: Any, __: float) -> _Response:
        """Return accepted n8n response for the outbound trigger call."""
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))
    result = await core.trigger_workflow(
        workflow_id="wf-1",
        event_type="agent.task.created",
        payload={"demo": True},
        correlation_id="corr-contract",
    )

    assert isinstance(result, dict)
    assert result["ok"] is True
    assert result["correlation_id"] == "corr-contract"
    assert result["event_id"]
