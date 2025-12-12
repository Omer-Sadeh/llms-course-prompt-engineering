"""
Main Entry Point.
"""
import logging
import sys
import os

# Add project root to path to allow running as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiment_runner import ExperimentRunner
from src.analysis import ResultAnalyzer
from src.utils.llm_client import OllamaClient, start_ollama_server
from src.config.config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Prompt Engineering Analysis Project")
    
    # Check Ollama connection first
    client = OllamaClient(base_url=config.llm.base_url)
    if not client.check_connection():
        logger.warning("Ollama is not reachable.")
        if not start_ollama_server():
             logger.error("Could not start Ollama server. Please start it manually with `ollama serve`.")
             sys.exit(1)
    
    # Model Selection
    available_models = client.list_models()
    if not available_models:
        logger.error("No models found in Ollama. Please run `ollama pull <model>` to install one.")
        sys.exit(1)
        
    print("\nAvailable Models:")
    for i, model in enumerate(available_models):
        print(f"{i + 1}. {model}")
        
    try:
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

    # Run Experiments
    try:
        from src.utils.metrics import SimilarityEvaluator
        from src.utils.data_generator import SyllogismGenerator
        
        # Instantiate dependencies
        evaluator = SimilarityEvaluator(model_name=config.experiment.embedding_model)
        generator = SyllogismGenerator(seed=config.experiment.seed)
        
        # Inject dependencies
        runner = ExperimentRunner(llm_client=client, evaluator=evaluator, generator=generator)
        runner.run_all_experiments()
    except Exception as e:
        logger.error(f"Experiment execution failed: {e}")
        sys.exit(1)
        
    # Analyze Results
    try:
        analyzer = ResultAnalyzer()
        analyzer.generate_report()
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

    logger.info("Project workflow completed successfully.")

if __name__ == "__main__":
    main()
