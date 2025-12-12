# Prompts Documentation

This document tracks the prompts used in the experiment strategies.

## 1. Baseline (Zero-Shot)
- **Purpose**: Establish a lower-bound performance metric.
- **Structure**: Raw question text.
- **Example**:
  ```
  Premise 1: All cats are mammals.
  Premise 2: All mammals are animals.
  Question: Are all cats animals?
  ```

## 2. Basic Prompt Engineering
- **Purpose**: Test the effect of a persona/system instruction.
- **System Message**: 
  "You are a logic expert. Answer the following syllogism question clearly and concisely. Start with 'Yes' or 'No'."
- **User Message**: [Question Text]

## 3. Few-Shot Learning
- **Purpose**: Provide context and expected output format to the model.
- **Structure**: 2 examples (1 valid, 1 invalid) followed by the target question.
- **Example**:
  ```
  Here are some examples of logic puzzles:

  Premise 1: All A are B.
  Premise 2: All B are C.
  Question: Are all A C?
  Answer: Yes...

  [Target Question]
  Answer:
  ```

## 4. Chain of Thought (CoT)
- **Purpose**: Encourage reasoning before answering.
- **Structure**: Question + "Let's think step by step to derive the correct answer."
- **Example**:
  ```
  [Question Text]
  Let's think step by step to derive the correct answer.
  ```

## Iterative Development Process

The prompt engineering process for this project followed these stages:

1.  **Baseline Establishment**: We started with raw questions to determine the model's innate capability.
2.  **Instruction Tuning**: We added persona and strict formatting instructions (Basic Strategy) to improve consistency.
3.  **Context Injection**: We introduced Few-Shot examples to guide the model's reasoning pattern.
4.  **Reasoning Activation**: We applied Chain of Thought (CoT) triggers to handle complex logic puzzles, observing significant improvements in accuracy.

## Failed Approaches

-   **Complex Persona Constraints**: Initially, we tried overly complex system prompts (e.g., "You are a PhD in Logic..."). This often confused smaller models or led to overly verbose outputs without improving accuracy.
-   **Negative Constraints**: Directing the model on what *not* to do (e.g., "Do not explain") was less effective than providing positive examples of the desired format.

## Best Practices Discovered

-   **Be Specific**: Clear, imperative instructions outperform polite requests.
-   **Show, Don't Just Tell**: Few-shot examples are the most powerful tool for enforcing output format.
-   **Step-by-Step**: For logic tasks, forcing the model to articulate steps (CoT) dramatically reduces hallucination errors.
