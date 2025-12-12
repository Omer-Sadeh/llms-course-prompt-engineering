# Cost Analysis

## Overview
This document outlines the estimated and actual costs associated with running the prompt engineering experiments. Since we utilize local inference (Ollama) and local embeddings, the direct monetary cost is minimal, primarily related to electricity and hardware amortization.

## Resource Usage
- **Compute**: Local CPU/GPU (M1/M2 or NVIDIA GPU).
- **Storage**: ~500MB for models and datasets.
- **Time**: approx. 5 minutes per 100 experiments.

## Token Estimation
Although we do not pay per token, tracking token usage is useful for estimating costs if we were to switch to a commercial provider (e.g., OpenAI API).

| Strategy | Avg Input Tokens | Avg Output Tokens | Est. Cost (OpenAI GPT-4o) |
| :--- | :--- | :--- | :--- |
| Baseline | 50 | 10 | $0.0003 |
| Basic | 80 | 10 | $0.0005 |
| Few-Shot | 300 | 10 | $0.0016 |
| Chain of Thought | 60 | 100 | $0.0018 |

**Total Estimated Cost for 1000 runs**: ~$5.00 (if using GPT-4o).
**Actual Cost**: $0.00 (Local Execution).

## Budget
See [budget.csv](./budget.csv) for a detailed breakdown of potential cloud costs vs local execution.
