from typing import Dict, List, Any
from src.core.interfaces import PromptStrategy
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
