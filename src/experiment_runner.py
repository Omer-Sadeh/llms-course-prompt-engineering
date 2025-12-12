"""
Experiment Runner Module.
"""
import logging
import pandas as pd
from typing import List, Dict, Any
from tqdm import tqdm
import time

from src.config.config import config
from src.utils.llm_client import OllamaClient
from src.utils.metrics import SimilarityEvaluator
from src.utils.data_generator import SyllogismGenerator

logger = logging.getLogger(__name__)

class ExperimentRunner:
    """Orchestrates the prompt engineering experiments."""

    def __init__(self):
        self.llm = OllamaClient(
            model=config.llm.model,
            temperature=config.llm.temperature,
            base_url=config.llm.base_url
        )
        self.evaluator = SimilarityEvaluator(model_name=config.experiment.embedding_model)
        self.generator = SyllogismGenerator(seed=config.experiment.seed)
        
        # Prepare datasets
        self.dataset = self.generator.generate_dataset(size=config.experiment.dataset_size)
        
        # Generate distinct few-shot examples
        self.few_shot_examples = self.generator.generate_dataset(size=4) # 2 valid, 2 invalid

    def run_all_experiments(self) -> pd.DataFrame:
        """Runs all defined strategies."""
        results = []
        
        strategies = [
            ("Baseline (Zero-Shot)", self._strategy_baseline),
            ("Basic Prompting", self._strategy_basic),
            ("Few-Shot", self._strategy_few_shot),
            ("Chain of Thought", self._strategy_cot)
        ]

        logger.info("Starting experiments...")
        
        for name, strategy_func in strategies:
            logger.info(f"Running strategy: {name}")
            for item in tqdm(self.dataset, desc=name):
                start_time = time.time()
                response = strategy_func(item)
                elapsed = time.time() - start_time
                
                distance = self.evaluator.calculate_distance(response, item['answer'])
                
                results.append({
                    "strategy": name,
                    "question": item['question'],
                    "ground_truth": item['answer'],
                    "model_output": response,
                    "vector_distance": distance,
                    "latency": elapsed
                })

        df = pd.DataFrame(results)
        self._save_results(df)
        return df

    def _save_results(self, df: pd.DataFrame):
        """Saves results to configured path."""
        config.paths.results.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(config.paths.results, index=False)
        logger.info(f"Results saved to {config.paths.results}")

    # --- Strategies ---

    def _strategy_baseline(self, item: Dict[str, str]) -> str:
        """Raw prompt, no system message."""
        return self.llm.generate(prompt=item['question'])

    def _strategy_basic(self, item: Dict[str, str]) -> str:
        """With specific system message."""
        system_msg = "You are a logic expert. Answer the following syllogism question clearly and concisely. Start with 'Yes' or 'No'."
        return self.llm.generate(prompt=item['question'], system=system_msg)

    def _strategy_few_shot(self, item: Dict[str, str]) -> str:
        """Includes examples in the prompt."""
        prompt = "Here are some examples of logic puzzles:\n\n"
        for ex in self.few_shot_examples:
            prompt += f"{ex['question']}\nAnswer: {ex['answer']}\n\n"
        
        prompt += f"Now solve this one:\n{item['question']}\nAnswer:"
        return self.llm.generate(prompt=prompt)

    def _strategy_cot(self, item: Dict[str, str]) -> str:
        """Chain of Thought prompting."""
        prompt = f"{item['question']}\nLet's think step by step to derive the correct answer."
        return self.llm.generate(prompt=prompt)

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    runner = ExperimentRunner()
    if runner.llm.check_connection():
        runner.run_all_experiments()
    else:
        logger.error("Could not connect to Ollama. Ensure it is running.")
