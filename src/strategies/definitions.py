from typing import Any, Dict, List

from src.core.registry import strategy_registry


@strategy_registry.register("Baseline (Zero-Shot)")
class BaselineStrategy:
    name = "Baseline (Zero-Shot)"
    description = "Raw prompt, no system message."

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        return llm_client.generate(prompt=item['question'])

@strategy_registry.register("Basic Prompting")
class BasicStrategy:
    name = "Basic Prompting"
    description = "With specific system message."

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        system_msg = "You are a logic expert. Answer the following syllogism question clearly and concisely. Start with 'Yes' or 'No'."
        return llm_client.generate(prompt=item['question'], system=system_msg)

@strategy_registry.register("Few-Shot")
class FewShotStrategy:
    name = "Few-Shot"
    description = "Includes examples in the prompt."

    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        prompt = "Here are some examples of logic puzzles:\n\n"
        for ex in self.examples:
            prompt += f"{ex['question']}\nAnswer: {ex['answer']}\n\n"
        
        prompt += f"Now solve this one:\n{item['question']}\nAnswer:"
        return llm_client.generate(prompt=prompt)

@strategy_registry.register("Chain of Thought")
class CoTStrategy:
    name = "Chain of Thought"
    description = "Chain of Thought prompting."

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        prompt = f"{item['question']}\nLet's think step by step to derive the correct answer."
        return llm_client.generate(prompt=prompt)

@strategy_registry.register("Self-Consistency")
class SelfConsistencyStrategy:
    name = "Self-Consistency"
    description = "Generates multiple CoT paths and selects the most frequent answer (Simulated with single path for now)."

    def execute(self, item: Dict[str, Any], llm_client: Any) -> str:
        # In a full implementation, we would generate k samples. 
        # For this prototype, we emphasize the instruction to be robust.
        prompt = (
            f"{item['question']}\n"
            "Think through this step-by-step. "
            "Double check your reasoning to ensure it is absolutely correct. "
            "Answer:"
        )
        return llm_client.generate(prompt=prompt)
