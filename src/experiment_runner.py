"""
Experiment Runner Module.
"""
import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config.config import config
from src.utils.llm_client import OllamaClient
from src.utils.metrics import SimilarityEvaluator
from src.utils.data_generator import SyllogismGenerator
from src.core.registry import strategy_registry
import src.strategies.definitions  # Import to register strategies

logger = logging.getLogger(__name__)

class ExperimentRunner:
    """Orchestrates the prompt engineering experiments."""

    def __init__(self, llm_client: Optional[OllamaClient] = None, 
                 evaluator: Optional[SimilarityEvaluator] = None, 
                 generator: Optional[SyllogismGenerator] = None):
        
        self.llm = llm_client or OllamaClient(
            model=config.llm.model,
            temperature=config.llm.temperature,
            base_url=config.llm.base_url
        )
        self.evaluator = evaluator or SimilarityEvaluator(model_name=config.experiment.embedding_model)
        self.generator = generator or SyllogismGenerator(seed=config.experiment.seed)
        
        # Prepare datasets
        self.dataset = self.generator.generate_dataset(size=config.experiment.dataset_size)
        
        # Generate distinct few-shot examples
        self.few_shot_examples = self.generator.generate_dataset(size=4) # 2 valid, 2 invalid

    def run_all_experiments(self) -> pd.DataFrame:
        """Runs all defined strategies."""
        results = []
        
        # Instantiate strategies from registry
        strategies = []
        for name in strategy_registry.list_all():
            if name == "Few-Shot":
                strategies.append((name, strategy_registry.create(name, examples=self.few_shot_examples)))
            else:
                strategies.append((name, strategy_registry.create(name)))

        logger.info(f"Starting experiments with strategies: {[s[0] for s in strategies]}")
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            for name, strategy_instance in strategies:
                logger.info(f"Running strategy: {name}")
                
                # Submit all tasks for this strategy
                future_to_item = {
                    executor.submit(self._process_single_item, item, name, strategy_instance): item 
                    for item in self.dataset
                }
                
                for future in tqdm(as_completed(future_to_item), total=len(self.dataset), desc=name):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Error processing item for strategy {name}: {e}")

        df = pd.DataFrame(results)
        self._save_results(df)
        return df

    def _process_single_item(self, item: Dict[str, str], strategy_name: str, strategy_instance: Any) -> Dict[str, Any]:
        """Process a single item with the given strategy."""
        start_time = time.time()
        response = strategy_instance.execute(item, self.llm)
        elapsed = time.time() - start_time
        
        distance = self.evaluator.evaluate(response, item['answer'])
        
        return {
            "strategy": strategy_name,
            "question": item['question'],
            "ground_truth": item['answer'],
            "model_output": response,
            "vector_distance": distance,
            "latency": elapsed
        }

    def _save_results(self, df: pd.DataFrame):
        """Saves results to configured path."""
        config.paths.results.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(config.paths.results, index=False)
        logger.info(f"Results saved to {config.paths.results}")

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    runner = ExperimentRunner()
    if runner.llm.check_connection():
        runner.run_all_experiments()
    else:
        logger.error("Could not connect to Ollama. Ensure it is running.")
