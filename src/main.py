"""
Main Entry Point.
"""
import argparse
import logging
import os
import sys
from typing import Optional

# Add project root to path to allow running as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis import ResultAnalyzer
from src.config.config import config
from src.experiment_runner import ExperimentRunner
from src.utils.llm_client import OllamaClient, start_ollama_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Prompt Engineering Analysis Experiment Runner",
        epilog="Use this CLI to run experiments with different LLM models and prompting strategies."
    )
    return parser.parse_args()

def setup_environment() -> Optional[OllamaClient]:
    """Checks and sets up the Ollama environment."""
    client = OllamaClient(base_url=config.llm.base_url)
    if not client.check_connection():
        logger.warning("Ollama is not reachable.")
        if not start_ollama_server():
             logger.error("Could not start Ollama server. Please start it manually with `ollama serve`.")
             return None
    return client

def select_model(client: OllamaClient) -> None:
    """Interactively selects the LLM model."""
    available_models = client.list_models()
    if not available_models:
        logger.error("No models found in Ollama. Please run `ollama pull <model>` to install one.")
        sys.exit(1)
        
    logger.info("Available Models:")
    for i, model in enumerate(available_models):
        logger.info(f"{i + 1}. {model}")
        
    try:
        # We still use input() for interaction, but log the prompt context
        logger.info(f"Prompting user for model selection (default: {config.llm.model})")
        choice = input(f"\nSelect a model (1-{len(available_models)}) [default: {config.llm.model}]: ").strip()
        if choice:
            idx = int(choice) - 1
            if 0 <= idx < len(available_models):
                selected_model = available_models[idx]
                logger.info(f"Selected model: {selected_model}")
                config.llm.model = selected_model
            else:
                logger.warning("Invalid selection. Using default model.")
        else:
             logger.info(f"Using default model: {config.llm.model}")
    except ValueError:
        logger.warning("Invalid input. Using default model.")

def run_experiments(client: OllamaClient) -> None:
    """Instantiates dependencies and runs experiments."""
    try:
        from src.utils.data_generator import SyllogismGenerator
        from src.utils.metrics import SimilarityEvaluator
        
        # Instantiate dependencies
        evaluator = SimilarityEvaluator(model_name=config.experiment.embedding_model)
        generator = SyllogismGenerator(seed=config.experiment.seed)
        
        # Inject dependencies
        runner = ExperimentRunner(llm_client=client, evaluator=evaluator, generator=generator)
        runner.run_all_experiments()
    except Exception as e:
        logger.error(f"Experiment execution failed: {e}")
        sys.exit(1)

def generate_report() -> None:
    """Analyzes results and generates a report."""
    try:
        analyzer = ResultAnalyzer()
        analyzer.generate_report()
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

def main():
    _ = parse_args()
    logger.info("Starting Prompt Engineering Analysis Project")
    
    client = setup_environment()
    if not client:
        sys.exit(1)
    
    select_model(client)
    run_experiments(client)
    generate_report()

    logger.info("Project workflow completed successfully.")

if __name__ == "__main__":
    main()