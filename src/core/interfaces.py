from typing import Protocol, Dict, Any, runtime_checkable

@runtime_checkable
class PromptStrategy(Protocol):
    """Protocol for prompt engineering strategies."""
    
    name: str
    description: str

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        """
        Executes the strategy for a single item.
        
        Args:
            item: The input data item (e.g., dictionary with 'question').
            llm_client: The LLM client to use for generation.
            
        Returns:
            The generated response string.
        """
        ...

@runtime_checkable
class MetricEvaluator(Protocol):
    """Protocol for evaluation metrics."""
    
    name: str

    def evaluate(self, prediction: str, reference: str) -> float:
        """
        Evaluates the prediction against the reference.
        
        Args:
            prediction: The model's output.
            reference: The ground truth.
            
        Returns:
            A float score (e.g., distance or similarity).
        """
        ...
