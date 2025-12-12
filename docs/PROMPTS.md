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
