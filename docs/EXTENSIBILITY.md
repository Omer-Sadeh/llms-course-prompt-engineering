# Extensibility Guide

This project is designed to be extensible, allowing researchers to easily add new prompt strategies and evaluation metrics.

## Adding a New Prompt Strategy

Prompt strategies are defined in the `ExperimentRunner` class within `src/experiment_runner.py`.

1.  **Define the Method**: Create a new method in `ExperimentRunner` with the signature `_strategy_<name>(self, item: Dict[str, str]) -> str`.
    ```python
    def _strategy_new_strategy(self, item: Dict[str, str]) -> str:
        """
        Description of your new strategy.
        """
        prompt = f"New Prompt Format: {item['question']}"
        return self.llm.generate(prompt=prompt)
    ```

2.  **Register the Strategy**: Add your new strategy to the `strategies` list in the `run_all_experiments` method.
    ```python
    strategies = [
        ("Baseline (Zero-Shot)", self._strategy_baseline),
        # ... existing strategies
        ("My New Strategy", self._strategy_new_strategy)
    ]
    ```

## Adding a New Metric

Metrics are handled by the `SimilarityEvaluator` in `src/utils/metrics.py`.

1.  **Extend the Class**: Add a new method to `SimilarityEvaluator`.
    ```python
    def calculate_new_metric(self, text1: str, text2: str) -> float:
        # Implementation of your metric
        return score
    ```

2.  **Update Runner**: Update `ExperimentRunner.run_all_experiments` to call this new metric and store the result in the `results` dictionary.

## Adding a New Dataset Type

To generate different types of logic puzzles, modify `src/utils/data_generator.py`.

1.  **Create Generator Class**: Create a new class or extend `SyllogismGenerator`.
2.  **Implement generate_dataset**: Ensure it returns a list of dictionaries with at least `question` and `answer` keys.
