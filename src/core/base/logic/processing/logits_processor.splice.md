# Class Breakdown: logits_processor

**File**: `src\core\base\logic\processing\logits_processor.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogitsProcessor`

**Line**: 62  
**Inherits**: Protocol  
**Methods**: 1

Protocol regarding logits processors.

A logits processor modifies the logits tensor before sampling.
It receives the past token IDs and current logits, returning
modified logits.

[TIP] **Suggested split**: Move to `logitsprocessor.py`

---

### 2. `LogitsProcessorList`

**Line**: 88  
**Methods**: 6

Composable list of logits processors.

Applies processors in order, passing the output of each to the next.

Example:
    >>> processors = LogitsProcessorList([
    ...     TemperatureProcessor(0.7),
...

[TIP] **Suggested split**: Move to `logitsprocessorlist.py`

---

### 3. `TemperatureProcessor`

**Line**: 131  
**Methods**: 2

Apply temperature scaling to logits.

Temperature < 1.0 makes distribution sharper (more deterministic)
Temperature > 1.0 makes distribution flatter (more random)
Temperature = 1.0 is unchanged

[TIP] **Suggested split**: Move to `temperatureprocessor.py`

---

### 4. `TopKProcessor`

**Line**: 166  
**Methods**: 2

Keep only top-k logits, set others to -inf.

This limits sampling to the k most likely tokens.

[TIP] **Suggested split**: Move to `topkprocessor.py`

---

### 5. `TopPProcessor`

**Line**: 216  
**Methods**: 2

Nucleus sampling - keep tokens with cumulative probability <= top_p.

This dynamically adjusts the number of considered tokens based on
their cumulative probability.

[TIP] **Suggested split**: Move to `toppprocessor.py`

---

### 6. `RepetitionPenaltyProcessor`

**Line**: 254  
**Methods**: 2

Penalize tokens that have already appeared.

penalty > 1.0 discourages repetition
penalty < 1.0 encourages repetition
penalty = 1.0 is unchanged

[TIP] **Suggested split**: Move to `repetitionpenaltyprocessor.py`

---

### 7. `NoBadWordsProcessor`

**Line**: 301  
**Methods**: 3

Block specific token sequences from being generated.

Given a list of "bad word" token sequences, this processor sets
their logits to -inf when they would complete a bad sequence.

[TIP] **Suggested split**: Move to `nobadwordsprocessor.py`

---

### 8. `MinLengthProcessor`

**Line**: 368  
**Methods**: 2

Prevent EOS token before minimum length is reached.

[TIP] **Suggested split**: Move to `minlengthprocessor.py`

---

### 9. `MaxLengthProcessor`

**Line**: 389  
**Methods**: 2

Force EOS token after maximum length is reached.

[TIP] **Suggested split**: Move to `maxlengthprocessor.py`

---

### 10. `PresencePenaltyProcessor`

**Line**: 411  
**Methods**: 2

Additive penalty regarding tokens that have appeared.

Unlike RepetitionPenalty (multiplicative), this adds a flat penalty
to any token that has appeared at least once.

[TIP] **Suggested split**: Move to `presencepenaltyprocessor.py`

---

### 11. `FrequencyPenaltyProcessor`

**Line**: 442  
**Methods**: 2

Penalty proportional to token frequency.

Tokens that appear more often receive a larger penalty.

[TIP] **Suggested split**: Move to `frequencypenaltyprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
