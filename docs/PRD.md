# Product Requirements Document (PRD)

## 1. Problem Statement
Prompt engineering is a critical skill for maximizing the utility of Large Language Models (LLMs). However, the effectiveness of different techniques is often anecdotal. This project aims to quantitatively analyze the impact of prompt engineering techniques (Zero-shot, Few-shot, Chain of Thought) on the model's performance in solving logic puzzles, measuring success via semantic vector distance.

## 2. Goals and KPIs
- **Goal**: Measure and visualize the improvement in model output quality across varying prompt complexities.
- **KPI**: Reduction in Mean Cosine Distance between model output and ground truth answers.
- **Target**: Achieve a >15% reduction in mean cosine distance for "Chain of Thought" prompting compared to the "Baseline" (Zero-shot) strategy.
- **Success Criteria**: The system must process 100 experiments in under 5 minutes on a standard M1/M2 machine.

## 3. Functional Requirements
- **Dataset Generation**: Automatically generate valid/invalid syllogisms (Parametrized size and difficulty).
- **Prompt Strategies**: Support Baseline, Basic (System), Few-Shot, and Chain of Thought prompts.
- **LLM Integration**: Connect to Ollama API with configurable model selection.
- **Evaluation**: Compute semantic similarity using Sentence Transformers (local execution).
- **Reporting**: Generate visualizations (Bar charts, distributions, and summary tables).

## 4. Non-Functional Requirements
- **Modularity**: Separation of data, client, metrics, and runner.
- **Reproducibility**: Seeded random generation for datasets and consistent sampling.
- **Robustness**: Handle API failures gracefully with retries and timeout management.
- **Performance**: Support concurrent experiment execution to minimize total runtime.

## 5. Constraints
- **Hardware**: Must run locally on consumer-grade hardware (e.g., Apple Silicon, 16GB RAM).
- **Dependencies**: All ML dependencies (Ollama, Sentence Transformers) must be capable of offline execution after initial download.
- **Cost**: No paid external APIs (OpenAI, Anthropic) for the core pipeline; strictly open-source local models.

## 6. Timeline
- **Phase 1: Core Infrastructure** (Completed - Dec 10, 2025)
    - Setup project structure, basic Ollama connectivity, and data generation.
- **Phase 2: Experiment Runner** (Completed - Dec 11, 2025)
    - Implement strategies and basic evaluation metrics.
- **Phase 3: Analysis** (Completed - Dec 12, 2025)
    - Generate plots and summary statistics.
- **Phase 4: Optimization & Robustness** (Target: Dec 15, 2025)
    - Implement multiprocessing for faster experiments.
    - Add comprehensive unit and integration tests (>80% coverage).
    - Setup CI/CD pipelines.
- **Phase 5: Extensibility Release** (Target: Dec 20, 2025)
    - Document plugin system for new strategies.
    - Release detailed research notebooks and cost analysis.
