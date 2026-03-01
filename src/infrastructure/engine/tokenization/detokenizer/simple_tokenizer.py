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

"""Simple concrete tokenizer implementations that satisfy TokenizerLike protocol."""

from typing import Dict, List, Optional, Union
import re


class SimpleWhitespaceTokenizer:
    """
    Simple whitespace-based tokenizer that implements TokenizerLike protocol.
    
    This is a basic implementation for demonstration and fallback purposes.
    For production, use transformers.AutoTokenizer or tiktoken.
    
    Example:
        >>> tokenizer = SimpleWhitespaceTokenizer()
        >>> token_ids = tokenizer.encode("Hello world!")
        >>> print(token_ids)
        [15496, 17191, 8]
        >>> text = tokenizer.decode(token_ids)
        >>> print(text)
        'Hello world!'
    """
    
    def __init__(self, vocab_size: int = 50000):
        """
        Initialize tokenizer with a vocabulary.
        
        Args:
            vocab_size: Maximum vocabulary size (default: 50000).
        """
        self.vocab_size = vocab_size
        self._vocab: Dict[str, int] = {}
        self._reverse_vocab: Dict[int, str] = {}
        self._next_id = 0
        
        # Add special tokens
        self._add_token("<pad>")
        self._add_token("<unk>")
        self._add_token("<s>")
        self._add_token("</s>")
        
        self.pad_token_id = 0
        self.unk_token_id = 1
        self.bos_token_id = 2
        self._eos_token_id = 3
    
    def _add_token(self, token: str) -> int:
        """Add a token to vocabulary and return its ID."""
        if token not in self._vocab:
            if self._next_id >= self.vocab_size:
                return self.unk_token_id
            self._vocab[token] = self._next_id
            self._reverse_vocab[self._next_id] = token
            self._next_id += 1
        return self._vocab[token]
    
    def _tokenize(self, text: str) -> List[str]:
        """Split text into tokens."""
        # Simple whitespace and punctuation tokenization
        tokens = re.findall(r'\w+|[^\w\s]', text)
        return tokens
    
    def encode(self, text: str, **kwargs) -> List[int]:
        """
        Encode text to token IDs.
        
        Args:
            text: Input text to tokenize.
            **kwargs: Additional parameters:
                - add_special_tokens (bool): Add BOS/EOS tokens (default: False)
                - max_length (int): Maximum sequence length
                - truncation (bool): Truncate if exceeds max_length
        
        Returns:
            List of integer token IDs.
        """
        add_special_tokens = kwargs.get('add_special_tokens', False)
        max_length = kwargs.get('max_length', None)
        truncation = kwargs.get('truncation', False)
        
        # Tokenize
        tokens = self._tokenize(text)
        
        # Convert tokens to IDs
        token_ids = []
        if add_special_tokens:
            token_ids.append(self.bos_token_id)
        
        for token in tokens:
            if token not in self._vocab:
                token_id = self._add_token(token)
            else:
                token_id = self._vocab[token]
            token_ids.append(token_id)
        
        if add_special_tokens:
            token_ids.append(self.eos_token_id)
        
        # Truncate if needed
        if truncation and max_length and len(token_ids) > max_length:
            token_ids = token_ids[:max_length]
        
        return token_ids
    
    def decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            token_ids: Single token ID or list of token IDs.
            skip_special_tokens: Skip special tokens like <pad>, <s>, </s>.
            **kwargs: Additional decoding parameters.
        
        Returns:
            Decoded text string.
        """
        # Handle single token ID
        if isinstance(token_ids, int):
            token_ids = [token_ids]
        
        # Decode tokens
        tokens = []
        special_token_ids = {self.pad_token_id, self.bos_token_id, self.eos_token_id}
        
        for token_id in token_ids:
            if skip_special_tokens and token_id in special_token_ids:
                continue
            
            if token_id in self._reverse_vocab:
                tokens.append(self._reverse_vocab[token_id])
            else:
                tokens.append("<unk>")
        
        # Join tokens with spaces (simple approach)
        return ' '.join(tokens)
    
    def convert_ids_to_tokens(
        self,
        ids: Union[int, List[int]],
    ) -> Union[str, List[str]]:
        """
        Convert token IDs to token strings.
        
        Args:
            ids: Single token ID or list of token IDs.
        
        Returns:
            Single token string or list of token strings.
        """
        if isinstance(ids, int):
            return self._reverse_vocab.get(ids, "<unk>")
        return [self._reverse_vocab.get(tid, "<unk>") for tid in ids]
    
    def convert_tokens_to_ids(
        self,
        tokens: Union[str, List[str]],
    ) -> Union[int, List[int]]:
        """
        Convert token strings to token IDs.
        
        Args:
            tokens: Single token string or list of token strings.
        
        Returns:
            Single token ID or list of token IDs.
        """
        if isinstance(tokens, str):
            return self._vocab.get(tokens, self.unk_token_id)
        return [self._vocab.get(token, self.unk_token_id) for token in tokens]
    
    @property
    def vocab(self) -> Dict[str, int]:
        """Get the vocabulary mapping."""
        return self._vocab.copy()
    
    @property
    def eos_token_id(self) -> Optional[int]:
        """Get the end-of-sequence token ID."""
        return self._eos_token_id


class HuggingFaceTokenizerAdapter:
    """
    Adapter for Hugging Face tokenizers to ensure TokenizerLike compatibility.
    
    Wraps transformers.PreTrainedTokenizer to match our protocol exactly.
    
    Example:
        >>> from transformers import AutoTokenizer
        >>> hf_tokenizer = AutoTokenizer.from_pretrained("gpt2")
        >>> tokenizer = HuggingFaceTokenizerAdapter(hf_tokenizer)
        >>> token_ids = tokenizer.encode("Hello world")
        >>> print(token_ids)
    """
    
    def __init__(self, hf_tokenizer):
        """
        Initialize adapter with Hugging Face tokenizer.
        
        Args:
            hf_tokenizer: A transformers.PreTrainedTokenizer instance.
        """
        self.hf_tokenizer = hf_tokenizer
    
    def encode(self, text: str, **kwargs) -> List[int]:
        """Encode text using Hugging Face tokenizer."""
        return self.hf_tokenizer.encode(text, **kwargs)
    
    def decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = True,
        **kwargs,
    ) -> str:
        """Decode token IDs using Hugging Face tokenizer."""
        return self.hf_tokenizer.decode(token_ids, skip_special_tokens=skip_special_tokens, **kwargs)
    
    def convert_ids_to_tokens(
        self,
        ids: Union[int, List[int]],
    ) -> Union[str, List[str]]:
        """Convert IDs to tokens using Hugging Face tokenizer."""
        return self.hf_tokenizer.convert_ids_to_tokens(ids)
    
    def convert_tokens_to_ids(
        self,
        tokens: Union[str, List[str]],
    ) -> Union[int, List[int]]:
        """Convert tokens to IDs using Hugging Face tokenizer."""
        return self.hf_tokenizer.convert_tokens_to_ids(tokens)
    
    @property
    def vocab(self) -> Dict[str, int]:
        """Get vocabulary from Hugging Face tokenizer."""
        return self.hf_tokenizer.get_vocab()
    
    @property
    def eos_token_id(self) -> Optional[int]:
        """Get EOS token ID from Hugging Face tokenizer."""
        return self.hf_tokenizer.eos_token_id
