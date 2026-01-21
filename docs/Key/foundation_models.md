# Foundation Models

## What are Foundation Models?
Foundation Models are large-scale AI models trained on vast amounts of data (often unlabeled) that can be adapted (e.g., fine-tuned) to a wide range of downstream tasks. Unlike traditional AI models designed for a single specific task (like a spam filter), foundation models learn broad representations of the world, language, or vision, serving as a "foundation" for many applications.

The term was popularized by the Stanford Institute for Human-Centered AI (HAI).

## Key Characteristics
1.  **Scale**: Trained on massive datasets (petabytes of text, billions of images) using huge compute resources.
2.  **Self-Supervision**: Typically trained using self-supervised learning objectives (like next-token prediction or masked language modeling) rather than requiring human-labeled data for every example.
3.  **Adaptability**: Can be adapted to tasks they weren't explicitly trained for via:
    *   **Zero-shot/Few-shot Learning**: Performing tasks with just a prompt.
    *   **Fine-tuning**: Updating weights on a small labeled dataset.
    *   **In-context Learning**: Learning from examples provided in the prompt.
4.  **Homogenization**: A single model architecture (like the Transformer) is used across many domains (text, image, audio), and a single trained model can replace many specialized models.

## Examples of Foundation Models

### Language (LLMs)
*   **GPT-4 (OpenAI)**: A multimodal model capable of reasoning, coding, and creative writing.
*   **Claude 3 (Anthropic)**: Known for large context windows and safety focus.
*   **Llama 3 (Meta)**: A powerful open-weights model family.
*   **BERT (Google)**: One of the first foundation models, widely used for understanding tasks (classification, entity recognition).

### Vision & Multimodal
*   **CLIP (OpenAI)**: Connects text and images, allowing for zero-shot image classification.
*   **Stable Diffusion (Stability AI)**: Generates images from text descriptions.
*   **Segment Anything Model (SAM)**: A foundation model for image segmentation.

### Audio
*   **Whisper (OpenAI)**: A foundation model for speech recognition and translation.

## The Paradigm Shift
*   **Pre-2018**: "Train a model for every task." (e.g., one model for translation, another for summarization).
*   **Post-2018**: "Train one model, adapt it to many tasks."

## Challenges
*   **Bias & Fairness**: They ingest biases present in the training data.
*   **Hallucination**: Generating plausible but incorrect information.
*   **Compute Cost**: Training and running these models requires significant hardware (GPUs).
*   **Evaluation**: It is difficult to comprehensively evaluate a model that can do "everything."
