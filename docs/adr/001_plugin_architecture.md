# ADR 001: Plugin Architecture for Strategies and Metrics

## Status
Accepted

## Context
The project requires extensibility to allow users to add new prompting strategies and evaluation metrics without modifying the core codebase. The previous implementation had hardcoded strategy methods in the `ExperimentRunner` class, making it difficult to extend and violating the Open/Closed Principle.

## Decision
We decided to implement a **Registry-based Plugin Architecture**.
- **Interfaces**: Defined `PromptStrategy` and `MetricEvaluator` protocols in `src/core/interfaces.py`.
- **Registry**: Implemented a generic `Registry` class in `src/core/registry.py` that allows registration of classes via decorators.
- **Implementations**: Moved concrete strategy implementations to `src/strategies/definitions.py`.

## Consequences
### Positive
- **Extensibility**: New strategies can be added by simply creating a class and decorating it with `@strategy_registry.register`.
- **Modularity**: Strategies are decoupled from the execution engine.
- **Testing**: Strategies can be tested in isolation more easily.

### Negative
- **Complexity**: Introduces a slight overhead in understanding the registry mechanism vs simple method calls.
- **Indirection**: The flow of control is slightly more indirect.
