# Prompt Engineering Effectiveness Analysis

## Description
This project analyzes the effectiveness of different prompt engineering techniques (Zero-shot, Few-shot, Chain of Thought) on Logic Puzzles (Syllogisms). It measures performance using vector distances between the model's output and the ground truth.

## Features
- **Dataset Generation**: Creates a dataset of logical syllogisms.
- **Multiple Prompting Strategies**: 
    - Baseline (Zero-shot)
    - Basic Prompt Engineering (System Prompt)
    - Few-Shot Learning
    - Chain of Thought (CoT)
- **Evaluation Metrics**: Uses Sentence Transformers to calculate semantic cosine distance.
- **Visualization**: Generates comparison plots of the effectiveness of each strategy.

## Installation

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. Ensure you have [Ollama](https://ollama.com/) installed and running with the `llama3` (or configured) model:
   ```bash
   ollama pull llama3
   ollama serve
   ```

## Configuration
Edit `config/settings.yaml` to change the model name, dataset size, or other parameters.

## Usage
Run the main experiment script:
```bash
python src/main.py
```
Results will be saved in `results/`.

## Testing
Run unit tests:
```bash
pytest
```

## Authors
Code Agent
