# Product Requirements Document (PRD)

## 1. Problem Statement
Prompt engineering is a critical skill for maximizing the utility of Large Language Models (LLMs). However, the effectiveness of different techniques is often anecdotal. This project aims to quantitatively analyze the impact of prompt engineering techniques (Zero-shot, Few-shot, Chain of Thought) on the model's performance in solving logic puzzles, measuring success via semantic vector distance.

## 2. Goals and KPIs
- **Goal**: Measure and visualize the improvement in model output quality across varying prompt complexities.
- **KPI**: Reduction in Mean Cosine Distance between model output and ground truth answers.

## 3. Functional Requirements
- **Dataset Generation**: Automatically generate valid/invalid syllogisms.
- **Prompt Strategies**: Support Baseline, Basic (System), Few-Shot, and Chain of Thought prompts.
- **LLM Integration**: Connect to Ollama API.
- **Evaluation**: Compute semantic similarity using Sentence Transformers.
- **Reporting**: Generate visualizations (Bar charts, distributions).

## 4. Non-Functional Requirements
- **Modularity**: Separation of data, client, metrics, and runner.
- **Reproducibility**: Seeded random generation.
- **Robustness**: Handle API failures gracefully.

## 5. Timeline
- **Phase 1**: Core Infrastructure (Done)
- **Phase 2**: Experiment Runner (Done)
- **Phase 3**: Analysis (Done)
