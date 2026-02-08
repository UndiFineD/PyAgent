
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_test_async_client_84e927afa8a5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'make_response'), 'missing make_response'
assert hasattr(mod, 'async_client'), 'missing async_client'
assert hasattr(mod, 'test_async_handle_response_returns_data'), 'missing test_async_handle_response_returns_data'
assert hasattr(mod, 'test_async_handle_response_app_code_error'), 'missing test_async_handle_response_app_code_error'
assert hasattr(mod, 'test_async_request_transport_error'), 'missing test_async_request_transport_error'
assert hasattr(mod, 'test_async_ping_returns_pong'), 'missing test_async_ping_returns_pong'
assert hasattr(mod, 'test_async_send_message_with_files_uses_multipart_payload'), 'missing test_async_send_message_with_files_uses_multipart_payload'
assert hasattr(mod, 'test_async_send_message_allows_nullable_blob_for_other_formats'), 'missing test_async_send_message_allows_nullable_blob_for_other_formats'
assert hasattr(mod, 'test_async_send_message_rejects_unknown_format'), 'missing test_async_send_message_rejects_unknown_format'
assert hasattr(mod, 'test_async_send_message_explicit_format_still_supported'), 'missing test_async_send_message_explicit_format_still_supported'
assert hasattr(mod, '_FakeOpenAIMessage'), 'missing _FakeOpenAIMessage'
assert hasattr(mod, '_FakeAnthropicMessage'), 'missing _FakeAnthropicMessage'
assert hasattr(mod, 'test_async_send_message_handles_openai_model_dump'), 'missing test_async_send_message_handles_openai_model_dump'
assert hasattr(mod, 'test_async_send_message_handles_anthropic_model_dump'), 'missing test_async_send_message_handles_anthropic_model_dump'
assert hasattr(mod, 'test_async_send_message_accepts_acontext_message'), 'missing test_async_send_message_accepts_acontext_message'
assert hasattr(mod, 'test_async_send_message_requires_file_field_when_file_provided'), 'missing test_async_send_message_requires_file_field_when_file_provided'
assert hasattr(mod, 'test_async_send_message_rejects_file_for_non_acontext_format'), 'missing test_async_send_message_rejects_file_for_non_acontext_format'
assert hasattr(mod, 'test_async_send_message_rejects_file_field_for_non_acontext_format'), 'missing test_async_send_message_rejects_file_field_for_non_acontext_format'
assert hasattr(mod, 'test_async_sessions_get_messages_forwards_format'), 'missing test_async_sessions_get_messages_forwards_format'
assert hasattr(mod, 'test_async_sessions_get_tasks_without_filters'), 'missing test_async_sessions_get_tasks_without_filters'
assert hasattr(mod, 'test_async_sessions_get_tasks_with_filters'), 'missing test_async_sessions_get_tasks_with_filters'
assert hasattr(mod, 'test_async_sessions_get_learning_status'), 'missing test_async_sessions_get_learning_status'
assert hasattr(mod, 'test_async_sessions_get_token_counts'), 'missing test_async_sessions_get_token_counts'
assert hasattr(mod, 'test_async_blocks_list_without_filters'), 'missing test_async_blocks_list_without_filters'
assert hasattr(mod, 'test_async_blocks_list_with_filters'), 'missing test_async_blocks_list_with_filters'
assert hasattr(mod, 'test_async_blocks_move_requires_payload'), 'missing test_async_blocks_move_requires_payload'
assert hasattr(mod, 'test_async_blocks_move_with_parent'), 'missing test_async_blocks_move_with_parent'
assert hasattr(mod, 'test_async_blocks_move_with_sort'), 'missing test_async_blocks_move_with_sort'
assert hasattr(mod, 'test_async_blocks_update_properties_requires_payload'), 'missing test_async_blocks_update_properties_requires_payload'
assert hasattr(mod, 'test_async_disks_create_hits_disk_endpoint'), 'missing test_async_disks_create_hits_disk_endpoint'
assert hasattr(mod, 'test_async_artifacts_aliases_disk_artifacts'), 'missing test_async_artifacts_aliases_disk_artifacts'
assert hasattr(mod, 'test_async_disk_artifacts_upsert_uses_multipart_payload'), 'missing test_async_disk_artifacts_upsert_uses_multipart_payload'
assert hasattr(mod, 'test_async_disk_artifacts_get_translates_query_params'), 'missing test_async_disk_artifacts_get_translates_query_params'
