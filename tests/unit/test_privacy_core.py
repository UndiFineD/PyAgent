from hypothesis import given, strategies as st
from src.logic.agents.security.core.PrivacyCore import PrivacyCore


class TestPrivacyCore:
    @given(st.text())
    def test_redact_text_idempotence(self, text):
        # Redacting twice should detect nothing new (unless patterns overlap weirdly, but generally stable)
        once = PrivacyCore.redact_text(text)
        twice = PrivacyCore.redact_text(once)
        assert once == twice

    def test_redact_specifics(self):
        email_text = "Contact me at user@example.com for details."
        assert "[EMAIL_REDACTED]" in PrivacyCore.redact_text(email_text)

        ipv4_text = "Server ip is 192.168.1.1"
        assert "[IP_REDACTED]" in PrivacyCore.redact_text(ipv4_text)

        # Simple API key sim
        key_text = "secret=abcde12345abcde12345"
        redacted = PrivacyCore.redact_text(key_text)
        assert "[REDACTED]" in redacted
        assert "abcde" not in redacted

    @given(
        st.recursive(
            st.text(),
            lambda children: st.lists(children) | st.dictionaries(st.text(), children),
            max_leaves=10,
        )
    )
    def test_scan_log_entry(self, data):
        # Just ensure it doesn't crash and returns same structure type
        result = PrivacyCore.scan_log_entry(data)
        assert isinstance(result, type(data))
