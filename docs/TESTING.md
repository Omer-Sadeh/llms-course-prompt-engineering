# Testing Documentation

## Overview
The project uses `pytest` for unit testing. Tests cover data generation, metric calculation, and configuration loading.

## Running Tests
```bash
pytest
```

## Test Coverage
- **Data Generator**: Verifies structure and logical consistency of generated syllogisms.
- **Metrics**: Verifies cosine distance calculation with orthogonal and identical vectors.
- **Config**: Verifies loading of YAML settings.

## Edge Cases
### 1. Ollama Unreachable
- **Behavior**: `ExperimentRunner` logs an error and exits gracefully if connection check fails.
- **Test**: Not automated (requires mocking network/integration test).

### 2. Empty Text for Metrics
- **Behavior**: `SimilarityEvaluator` returns distance 1.0 (max dissimilarity) to prevent crashing.
- **Test**: Verified in manual checks.

### 3. Missing Config File
- **Behavior**: `Config.load` raises `FileNotFoundError`.
- **Test**: `tests/test_config.py`.
