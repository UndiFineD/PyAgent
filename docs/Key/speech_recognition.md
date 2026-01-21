# Speech Recognition (ASR)

Automatic Speech Recognition (ASR) is the task of converting spoken audio into text.

## 1. Traditional Approaches

*   **HMM-GMM**: Hidden Markov Models combined with Gaussian Mixture Models. Modeled speech as a sequence of states (phonemes).
*   **Challenges**: Required complex feature engineering (MFCCs) and separate acoustic/language models.

## 2. End-to-End Deep Learning

*   **CTC (Connectionist Temporal Classification)**:
    *   Solves the alignment problem (audio is longer than text).
    *   Allows the network to output "blank" tokens or repeat characters, which are then collapsed (e.g., "h-he-ll-l--o" -> "hello").
*   **RNN-T (Recurrent Neural Network Transducer)**:
    *   Standard for streaming ASR (e.g., Siri/Google Assistant).
    *   Predicts the next character based on both the audio and the previous characters.

## 3. Whisper (OpenAI)

*   **Architecture**: A standard Transformer Encoder-Decoder trained on 680,000 hours of multilingual data.
*   **Multitask**: It doesn't just do ASR. It can do Translation, Language Identification, and Voice Activity Detection based on special "Task Tokens" at the start of the sequence.
*   **Robustness**: Works well in noisy environments and with accents because it was trained on diverse, "weakly supervised" internet audio.
