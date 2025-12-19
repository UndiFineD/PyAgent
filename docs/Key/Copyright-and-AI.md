# Copyright and AI

## The Two Main Legal Battles
The intersection of AI and Copyright Law focuses on two distinct questions:
1.  **Input**: Is it legal to train AI models on copyrighted data without permission?
2.  **Output**: Can AI-generated content be copyrighted?

## 1. Training Data (Input)
*   **The Issue**: AI models (LLMs, Image Generators) are trained on billions of images and texts scraped from the internet, much of which is copyrighted.
*   **The Defense (Fair Use)**: AI companies (OpenAI, Google, Stability AI) argue that training is **Fair Use** (in the US) or falls under **Text and Data Mining (TDM)** exceptions (in the EU/UK).
    *   They argue the model "reads" the data to learn patterns (facts/ideas), which are not copyrightable, rather than "copying" the expression.
    *   They compare it to a human student reading a library of books to learn how to write.
*   **The Prosecution**: Artists and Authors (New York Times, Getty Images) argue that:
    *   The models compete directly with the original works.
    *   The models can sometimes memorize and reproduce training data exactly (regurgitation).
    *   This constitutes massive commercial infringement.

## 2. AI-Generated Content (Output)
*   **US Position**: The US Copyright Office has ruled that **AI-generated content is NOT copyrightable**.
    *   Copyright requires "human authorship."
    *   Prompts are considered "instructions" to a machine, not creative control.
    *   *Exception*: If a human significantly modifies the AI output, the *human modifications* can be copyrighted, but not the underlying AI generation.
*   **Other Jurisdictions**:
    *   **UK**: Offers some protection for computer-generated works.
    *   **China**: Has granted copyright to some AI-generated images where the human input (prompting/selection) was deemed sufficient.

## Emerging Solutions
*   **Opt-Out**: Standards like `robots.txt` or C2PA allowing creators to block AI scrapers.
*   **Licensed Data**: Companies (like Adobe Firefly) training only on public domain or licensed stock images to avoid legal risk.
