# Natural Language Understanding (NLU)

While LLMs generate text (NLG), NLU focuses on extracting structured meaning from text.

## 1. Core Tasks

*   **NER (Named Entity Recognition)**: Identifying and classifying entities.
    *   "Elon Musk (PERSON) founded SpaceX (ORG) in 2002 (DATE)."
*   **Sentiment Analysis**: Determining the emotional tone (Positive, Negative, Neutral).
*   **POS Tagging (Part-of-Speech)**: Labeling words as Noun, Verb, Adjective, etc.
*   **Text Classification**: Assigning a category to a document (e.g., Spam vs. Ham, Sports vs. Politics).

## 2. Evolution

*   **Rule-Based**: Regular Expressions (Regex) and dictionaries.
*   **Statistical (NLP)**: Naive Bayes, SVMs using Bag-of-Words features.
*   **Deep Learning (BERT)**:
    *   BERT (Bidirectional Encoder Representations from Transformers) revolutionized NLU.
    *   Unlike GPT (which reads left-to-right), BERT reads the entire sentence at once to understand context from both directions.
    *   Standard workflow: Pre-train BERT on Wikipedia -> Fine-tune on specific NLU task.

## 3. Zero-Shot NLU

Modern LLMs can perform NLU tasks without specific fine-tuning.
*   **Prompt**: "Extract all companies from the following text and output them as a JSON list."
*   **Result**: `["SpaceX", "Tesla", "Neuralink"]`.
