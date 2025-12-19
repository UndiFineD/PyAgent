# Expert Systems

## Overview
**Expert Systems** were the dominant form of AI in the 1980s. Unlike modern Machine Learning (which learns from data), Expert Systems were **Symbolic AI** designed to mimic the decision-making ability of a human expert using explicit rules.

## Architecture
1.  **Knowledge Base**: A collection of facts and rules (`IF-THEN` statements) extracted from human experts.
    *   *Example*: `IF (fever > 102) AND (rash = True) THEN (diagnosis = measles)`.
2.  **Inference Engine**: The logic component that applies the rules to the known facts to deduce new facts.
    *   **Forward Chaining**: Start with facts and apply rules to reach a conclusion (Data-driven).
    *   **Backward Chaining**: Start with a hypothesis (Goal) and look for facts to support it (Goal-driven).

## Famous Examples
*   **MYCIN (1970s)**: Designed to diagnose bacterial infections and recommend antibiotics. It outperformed junior doctors but was never used legally due to liability issues.
*   **DENDRAL (1965)**: Analyzed mass spectrometry data to identify chemical structures. Considered the first expert system.
*   **XCON (R1)**: Used by DEC to automatically configure VAX computer systems based on customer orders. Saved millions of dollars.

## Limitations (Why they failed)
*   **The Knowledge Acquisition Bottleneck**: Extracting rules from human experts is slow, difficult, and expensive. Experts often can't articulate *how* they know something (intuition).
*   **Brittleness**: They couldn't handle uncertainty or edge cases well. If a rule didn't exist, the system failed completely.
*   **Maintenance**: As the number of rules grew (thousands), the interactions became impossible to debug.

## Legacy
While "Expert Systems" are dead, the concept lives on in **Business Rules Engines** (e.g., Drools) used in banking for loan approval and insurance underwriting.
