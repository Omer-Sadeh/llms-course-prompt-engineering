"""
Script to run sensitivity analysis varying temperature and dataset size.
"""
import logging
import pandas as pd
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiment_runner import ExperimentRunner
from src.config.config import config
from src.utils.llm_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Sensitivity Analysis")
    
    temperatures = [0.0, 0.5, 1.0]
    # We reduce dataset size for speed in this demo script, or keep it if capable.
    # config.experiment.dataset_size is default.
    
    results_all = []
    
    base_model = config.llm.model
    original_temp = config.llm.temperature
    
    try:
        for temp in temperatures:
            logger.info(f"Running experiments with Temperature={temp}")
            
            # Update config (runtime only)
            config.llm.temperature = temp
            
            # Re-init client with new temp
            client = OllamaClient(model=base_model, temperature=temp, base_url=config.llm.base_url)
            
            # Run experiments
            runner = ExperimentRunner(llm_client=client)
            df = runner.run_all_experiments()
            
            df['temperature'] = temp
            results_all.append(df)
            
        final_df = pd.concat(results_all, ignore_index=True)
        
        output_path = config.paths.results.parent / "sensitivity_results.csv"
        final_df.to_csv(output_path, index=False)
        logger.info(f"Sensitivity analysis complete. Results saved to {output_path}")
        
    finally:
        # Restore config
        config.llm.temperature = original_temp

if __name__ == "__main__":
    main()
