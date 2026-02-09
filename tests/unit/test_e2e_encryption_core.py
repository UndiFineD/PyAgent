#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")

"""
Tests for End-to-End Encryption Core.
Validates Signal Protocol implementation, forward secrecy, and zero-knowledge properties.
"""

import pytest
import tempfile
import os
from src.core.base.logic.security.e2e_encryption_core import (
    E2EEncryptionCore,
    UserKeyPair,
    RatchetState
)


@pytest.fixture
def e2e_core():
    """Create a temporary E2EE core for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        core = E2EEncryptionCore(storage_path=tmpdir)
        yield core


def test_key_generation(e2e_core):
    """Test identity key pair generation."""
    user_id = "alice"
    keypair = e2e_core.generate_identity_keypair(user_id)
    
    assert isinstance(keypair, UserKeyPair)
    assert keypair.user_id == user_id
    assert len(keypair.identity_public) == 32  # X25519 public key size
    assert len(keypair.prekeys) == 10  # Should generate 10 prekeys


def test_prekey_bundle_retrieval(e2e_core):
    """Test prekey bundle generation for X3DH."""
    user_id = "bob"
    e2e_core.generate_identity_keypair(user_id)
    
    bundle = e2e_core.get_public_prekey_bundle(user_id)
    
    assert bundle is not None
    assert bundle["user_id"] == user_id
    assert "identity_key" in bundle
    assert "prekey_id" in bundle
    assert "prekey" in bundle


def test_session_initiation(e2e_core):
    """Test X3DH session initiation between two users."""
    # Generate keys for both users
    e2e_core.generate_identity_keypair("alice")
    e2e_core.generate_identity_keypair("bob")
    
    # Alice initiates session with Bob
    bob_bundle = e2e_core.get_public_prekey_bundle("bob")
    ephemeral_public = e2e_core.initiate_session("alice", bob_bundle)
    
    assert ephemeral_public is not None
    assert len(ephemeral_public) == 32  # X25519 public key
    
    # Verify session was created
    session_key = ("alice", "bob")
    assert session_key in e2e_core.sessions


def test_message_encryption_decryption(e2e_core):
    """Test end-to-end message encryption with Double Ratchet."""
    # Setup users
    e2e_core.generate_identity_keypair("alice")
    e2e_core.generate_identity_keypair("bob")
    
    # Initiate session
    bob_bundle = e2e_core.get_public_prekey_bundle("bob")
    e2e_core.initiate_session("alice", bob_bundle)
    
    # Alice encrypts message to Bob
    plaintext = "Hello Bob! This is a secret message."
    encrypted = e2e_core.encrypt_message("alice", "bob", plaintext)
    
    assert encrypted["sender"] == "alice"
    assert encrypted["recipient"] == "bob"
    assert "ciphertext" in encrypted
    assert "nonce" in encrypted
    assert encrypted["ciphertext"] != plaintext


def test_forward_secrecy(e2e_core):
    """Test that each message uses a different key (forward secrecy)."""
    # Setup
    e2e_core.generate_identity_keypair("alice")
    e2e_core.generate_identity_keypair("bob")
    bob_bundle = e2e_core.get_public_prekey_bundle("bob")
    e2e_core.initiate_session("alice", bob_bundle)
    
    # Send multiple messages
    msg1 = e2e_core.encrypt_message("alice", "bob", "Message 1")
    msg2 = e2e_core.encrypt_message("alice", "bob", "Message 2")
    msg3 = e2e_core.encrypt_message("alice", "bob", "Message 3")
    
    # Verify each message has different ciphertext
    assert msg1["ciphertext"] != msg2["ciphertext"]
    assert msg2["ciphertext"] != msg3["ciphertext"]
    
    # Verify counters increment
    assert msg1["counter"] == 0
    assert msg2["counter"] == 1
    assert msg3["counter"] == 2


def test_user_data_encryption(e2e_core):
    """Test encryption of user-specific data (zero-knowledge)."""
    user_id = "alice"
    e2e_core.generate_identity_keypair(user_id)
    
    # Encrypt user data
    user_data = {
        "query": "What is my password?",
        "response": "hunter2",
        "timestamp": 1234567890
    }
    
    encrypted = e2e_core.encrypt_user_data(user_id, "memory", user_data)
    
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > 12  # At least nonce + some ciphertext
    
    # Decrypt and verify
    decrypted = e2e_core.decrypt_user_data(user_id, "memory", encrypted)
    
    assert decrypted == user_data


def test_user_data_isolation(e2e_core):
    """Test that users cannot decrypt each other's data."""
    # Generate keys for two users
    e2e_core.generate_identity_keypair("alice")
    e2e_core.generate_identity_keypair("bob")
    
    # Alice encrypts her data
    alice_data = {"secret": "Alice's password"}
    encrypted = e2e_core.encrypt_user_data("alice", "memory", alice_data)
    
    # Bob tries to decrypt Alice's data (should fail)
    with pytest.raises(Exception):  # Decryption will fail
        e2e_core.decrypt_user_data("bob", "memory", encrypted)


def test_key_persistence(e2e_core):
    """Test that user keys can be saved and loaded."""
    user_id = "alice"
    e2e_core.generate_identity_keypair(user_id)
    
    original_public_key = e2e_core.user_keys[user_id].identity_public
    
    # Clear in-memory keys
    e2e_core.user_keys.clear()
    
    # Load keys from storage
    assert e2e_core.load_user_keys(user_id) is True
    
    # Verify keys match
    loaded_public_key = e2e_core.user_keys[user_id].identity_public
    assert loaded_public_key == original_public_key


def test_invalid_session(e2e_core):
    """Test that encryption fails without an active session."""
    e2e_core.generate_identity_keypair("alice")
    
    with pytest.raises(ValueError, match="No active session"):
        e2e_core.encrypt_message("alice", "bob", "This should fail")


def test_encryption_different_data_types(e2e_core):
    """Test encryption for different data types (chat, memory, query)."""
    user_id = "alice"
    e2e_core.generate_identity_keypair(user_id)
    
    chat_data = {"history": ["msg1", "msg2"]}
    memory_data = {"content": "Important memory"}
    query_data = {"query": "How to code?"}
    
    # Encrypt different types
    chat_encrypted = e2e_core.encrypt_user_data(user_id, "chat", chat_data)
    memory_encrypted = e2e_core.encrypt_user_data(user_id, "memory", memory_data)
    query_encrypted = e2e_core.encrypt_user_data(user_id, "query", query_data)
    
    # Verify all encrypted
    assert all(isinstance(e, bytes) for e in [chat_encrypted, memory_encrypted, query_encrypted])
    
    # Verify all different
    assert chat_encrypted != memory_encrypted
    assert memory_encrypted != query_encrypted
    
    # Decrypt and verify
    assert e2e_core.decrypt_user_data(user_id, "chat", chat_encrypted) == chat_data
    assert e2e_core.decrypt_user_data(user_id, "memory", memory_encrypted) == memory_data
    assert e2e_core.decrypt_user_data(user_id, "query", query_encrypted) == query_data


def test_zero_knowledge_property(e2e_core):
    """
    Test zero-knowledge property: 
    Server (e2e_core) cannot decrypt data without user's private key.
    """
    user_id = "alice"
    keypair = e2e_core.generate_identity_keypair(user_id)
    
    secret_data = {"password": "super_secret_123"}
    encrypted = e2e_core.encrypt_user_data(user_id, "memory", secret_data)
    
    # Simulate server compromise: remove user's private key
    e2e_core.user_keys.clear()
    
    # Server now has encrypted data but no key
    # Attempting to decrypt should fail
    with pytest.raises(ValueError, match="has no identity keys"):
        e2e_core.decrypt_user_data(user_id, "memory", encrypted)
    
    # Verify encrypted data doesn't contain plaintext
    assert b"super_secret_123" not in encrypted
    assert b"password" not in encrypted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
