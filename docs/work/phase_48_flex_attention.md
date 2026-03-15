# Phase 48: FlexAttention & Tree Attention ✨

**Status**: IN-PROGRESS  
**Start Date**: 2026-01-21  
**Goal**: Advanced attention backends with FlexAttention and Tree Attention support.

---

## 🎯 Objectives
- Implement [FlexAttentionBackend.py](src/inference/backends/attention/flex_attention_backend.py) using PyTorch 2.5+ flex_attention.
- Implement [TreeAttentionBackend.py](src/inference/backends/attention/tree_attention_backend.py) for speculation trees.
- Implement [LinearAttentionBackend.py](src/inference/backends/attention/linear_attention_backend.py) for linear complexity.
- Implement [GDNAttention.py](src/inference/backends/attention/gdn_attention.py) for probabilistic attention.

## 🏗️ Modules Progress

| Module | Purpose | Status |
| :--- | :--- | :--- |
| `flex_attention_backend.py` | FlexAttention API wrapper | ⏳ NOT STARTED |
| `tree_attention_backend.py` | Tree-structured masks | ⏳ NOT STARTED |
| `linear_attention_backend.py` | Linear complexity attention | ⏳ NOT STARTED |
| `gdn_attention.py` | Probabilistic attention | ⏳ NOT STARTED |

## 🧪 Testing State
- FlexAttention block mask tests
- Tree attention branch scoring tests
- Linear attention causal masking tests
- GDN uncertainty estimation tests

## 🦀 Rust Accelerations
- `flex_attention_mask_rust`
- `tree_attention_paths_rust`
- `linear_attention_feature_rust`
- `attention_score_mod_rust`
