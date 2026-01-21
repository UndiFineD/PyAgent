# Audio Generation

Generating audio is harder than text because audio is high-dimensional (44,100 samples per second) and continuous.

## 1. Text-to-Speech (TTS)

*   **Concatenative (Old)**: Gluing together recorded snippets of speech. Robotic.
*   **Parametric (Statistical)**: Predicting acoustic features (spectrograms) and using a Vocoder to turn them into audio.
*   **Neural TTS (Tacotron, FastSpeech)**: End-to-end Deep Learning.
    *   **Encoder**: Text -> Phonemes -> Mel-Spectrogram.
    *   **Vocoder (WaveNet, HiFi-GAN)**: Mel-Spectrogram -> Waveform.

## 2. Music Generation

*   **Symbolic (MIDI)**: Generating notes (C4, E4, G4). Easy (like text generation) but lacks nuance (timbre, performance).
*   **Audio (Raw Waveform)**: Generating the actual sound.
    *   **MusicGen (Meta)**: Uses EnCodec to compress audio into discrete tokens, then uses a Transformer to predict the next token (like GPT for audio).
    *   **Jukebox (OpenAI)**: Generates raw audio at different timescales.

## 3. AudioLDM (Latent Diffusion for Audio)

Applying Stable Diffusion to audio.
1.  Convert Audio -> Mel-Spectrogram (Image-like).
2.  Compress into Latent Space (VAE).
3.  Train a Diffusion model to denoise the latents conditioned on text ("A jazz saxophone solo").
4.  Decode back to audio.

## 4. Whisper (Speech-to-Text)

Not generation, but critical. OpenAI's Whisper is a Transformer trained on 680k hours of multilingual audio. It treats the spectrogram as an image and predicts the text transcript.
