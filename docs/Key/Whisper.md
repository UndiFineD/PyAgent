# Whisper

## Overview
**Whisper** is a general-purpose speech recognition model released by OpenAI in 2022. It is a Transformer-based Encoder-Decoder model trained on 680,000 hours of multilingual and multitask supervised data collected from the web.

## Key Differentiator: Weak Supervision at Scale
Traditional ASR (Automatic Speech Recognition) models were trained on small, carefully curated datasets (like LibriSpeech). Whisper was trained on a massive, noisy dataset.
*   **Robustness**: Because it was trained on diverse audio (accents, background noise, technical language), it is incredibly robust "out of the box" without needing fine-tuning.
*   **Multitask**: The model is trained to perform multiple tasks depending on special tokens fed to the decoder:
    *   `<|transcribe|>`: Speech to Text.
    *   `<|translate|>`: Speech to English Text.
    *   `<|startoftranscript|>`: Detect language.

## Architecture
It uses a standard Transformer Encoder-Decoder architecture (similar to Seq2Seq).
1.  **Input**: Log-Mel Spectrogram of the audio (30-second chunks).
2.  **Encoder**: Processes the audio features.
3.  **Decoder**: Autoregressively predicts the text tokens, conditioned on the encoder output and previous tokens.

## Impact
Whisper democratized high-quality speech recognition. It is open-source and runs locally, enabling developers to build voice interfaces, transcription services, and subtitle generators without relying on paid cloud APIs.
