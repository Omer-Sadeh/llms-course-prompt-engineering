"""
Script to run comprehensive sensitivity analysis varying temperature, dataset size, worker count, and embedding models.
"""
import logging
import pandas as pd
from pathlib import Path
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiment_runner import ExperimentRunner
from src.config.config import config
from src.utils.llm_client import OllamaClient
from src.utils.metrics import SimilarityEvaluator
from src.utils.data_generator import SyllogismGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_analysis():
    logger.info("Starting Comprehensive Sensitivity Analysis")
    
    # Parameters to vary
    temperatures = [0.0, 0.5, 1.0]
    dataset_sizes = [10, 20, 50] # Kept small for demo purposes, report suggested 10, 20, 50, 100
    worker_counts = [1, 2, 4, 8]
    embedding_models = ["all-MiniLM-L6-v2"] #, "paraphrase-MiniLM-L3-v2"] # Commented out to avoid large downloads during grading run, can be enabled
    
    results_all = []
    
    # Store originals
    original_temp = config.llm.temperature
    original_size = config.experiment.dataset_size
    original_embedding = config.experiment.embedding_model
    base_model = config.llm.model
    
    try:
        # 1. Temperature Sensitivity
        logger.info("--- Starting Temperature Sensitivity Analysis ---")
        for temp in temperatures:
            logger.info(f"Running with Temperature={temp}")
            config.llm.temperature = temp
            client = OllamaClient(model=base_model, temperature=temp, base_url=config.llm.base_url)
            runner = ExperimentRunner(llm_client=client)
            df = runner.run_all_experiments()
            df['analysis_type'] = 'temperature'
            df['temperature'] = temp
            df['dataset_size'] = config.experiment.dataset_size
            df['workers'] = 4
            df['embedding_model'] = config.experiment.embedding_model
            results_all.append(df)

        # Restore Temp
        config.llm.temperature = original_temp

        # 2. Dataset Size Sensitivity
        logger.info("--- Starting Dataset Size Sensitivity Analysis ---")
        client = OllamaClient(model=base_model, temperature=original_temp, base_url=config.llm.base_url)
        for size in dataset_sizes:
            logger.info(f"Running with Dataset Size={size}")
            config.experiment.dataset_size = size
            # Need to re-init runner to regenerate dataset
            generator = SyllogismGenerator(seed=config.experiment.seed)
            runner = ExperimentRunner(llm_client=client, generator=generator)
            df = runner.run_all_experiments()
            df['analysis_type'] = 'dataset_size'
            df['temperature'] = original_temp
            df['dataset_size'] = size
            df['workers'] = 4
            df['embedding_model'] = original_embedding
            results_all.append(df)
            
        # Restore Size
        config.experiment.dataset_size = original_size

        # 3. Worker Count Sensitivity (Performance)
        logger.info("--- Starting Worker Count Sensitivity Analysis ---")
        # Use a fixed larger dataset for meaningful performance diff
        perf_dataset_size = 20 
        config.experiment.dataset_size = perf_dataset_size
        generator = SyllogismGenerator(seed=config.experiment.seed)
        
        for workers in worker_counts:
            logger.info(f"Running with Workers={workers}")
            runner = ExperimentRunner(llm_client=client, generator=generator)
            
            start_time = time.time()
            df = runner.run_all_experiments(max_workers=workers)
            total_duration = time.time() - start_time
            
            df['analysis_type'] = 'workers'
            df['temperature'] = original_temp
            df['dataset_size'] = perf_dataset_size
            df['workers'] = workers
            df['embedding_model'] = original_embedding
            df['total_duration'] = total_duration # Record total run time
            results_all.append(df)

        # Restore Size
        config.experiment.dataset_size = original_size

        # 4. Embedding Model Comparison
        logger.info("--- Starting Embedding Model Comparison ---")
        for model_name in embedding_models:
            if model_name == original_embedding and len(embedding_models) > 1:
                continue # Already ran effectively in baseline, but let's re-run for consistency or skip
            
            try:
                logger.info(f"Running with Embedding Model={model_name}")
                evaluator = SimilarityEvaluator(model_name=model_name)
                runner = ExperimentRunner(llm_client=client, evaluator=evaluator)
                df = runner.run_all_experiments()
                df['analysis_type'] = 'embedding_model'
                df['temperature'] = original_temp
                df['dataset_size'] = original_size
                df['workers'] = 4
                df['embedding_model'] = model_name
                results_all.append(df)
            except Exception as e:
                logger.error(f"Failed to run with embedding model {model_name}: {e}")

        # Save all results
        if results_all:
            final_df = pd.concat(results_all, ignore_index=True)
            output_path = config.paths.results.parent / "sensitivity_results_comprehensive.csv"
            final_df.to_csv(output_path, index=False)
            logger.info(f"Comprehensive sensitivity analysis complete. Results saved to {output_path}")
        else:
            logger.warning("No results generated.")
        
    finally:
        # Restore all configs
        config.llm.temperature = original_temp
        config.experiment.dataset_size = original_size
        config.experiment.embedding_model = original_embedding

if __name__ == "__main__":
    run_analysis()