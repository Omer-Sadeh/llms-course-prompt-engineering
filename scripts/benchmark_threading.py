"""
Benchmark script to measure threading performance vs sequential execution.
"""
import time
import logging
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy I/O bound task
def dummy_io_task(duration: float) -> float:
    time.sleep(duration)
    return duration

def run_sequential(tasks: List[float]) -> float:
    start_time = time.time()
    for duration in tasks:
        dummy_io_task(duration)
    return time.time() - start_time

def run_threaded(tasks: List[float], workers: int) -> float:
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(dummy_io_task, tasks))
    return time.time() - start_time

def main():
    logger.info("Starting performance benchmark...")
    
    # Configuration
    num_tasks = 20
    task_duration = 0.5 # seconds
    tasks = [task_duration] * num_tasks
    max_workers = 4
    
    logger.info(f"Configuration: {num_tasks} tasks, {task_duration}s per task, {max_workers} workers.")
    
    # Sequential Run
    logger.info("Running sequential benchmark...")
    seq_time = run_sequential(tasks)
    logger.info(f"Sequential time: {seq_time:.4f}s")
    
    # Threaded Run
    logger.info("Running threaded benchmark...")
    par_time = run_threaded(tasks, workers=max_workers)
    logger.info(f"Threaded time: {par_time:.4f}s")
    
    # Analysis
    speedup = seq_time / par_time
    results = {
        "sequential_time": seq_time,
        "threaded_time": par_time,
        "speedup": speedup,
        "efficiency": speedup / max_workers
    }
    
    logger.info(f"Speedup: {speedup:.2f}x")
    
    # Save results
    output_path = Path("results/benchmarks.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
