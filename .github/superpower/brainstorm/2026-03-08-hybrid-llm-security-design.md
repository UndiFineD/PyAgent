# Hybrid Execution & Security Architecture Design

## Section 5: Hybrid Execution & Security Architecture

1. **Local vs. Remote LLM Routing:**
   - **Environment Agnostic:** The system will dynamically switch between local inference (e.g., vLLM or Ollama) and remote APIs.
   - **Data Sanitization:** When requesting remote access, any outbound context is first scrubbed. Shared memory is decoupled so remote endpoints never receive the raw user data or proprietary agent logic.
2. **Dedicated Rust Security Core:**
   - A new Rust-based bridge (`rust_core/security/`) will intercept read/write calls to the `AgentStateManager`.
   - **Inline Encryption:** All user data, agent states, and shared memory blocks are encrypted and decrypted in real-time by the Rust layer to prevent remote tampering.
   - **Key Lifecycle Management:** The Rust core will autonomously manage the monthly key rotation, ensuring that old data is securely re-keyed without blocking the main event loops.
3. **Infrastructure Constraints:**
   - The data persistence layer mandates RAID10 configuration, offering both high IOPS for the shared memory architecture and strict redundancy for the encrypted payloads.