"""
Analysis and Visualization Module.
"""
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.config.config import config

logger = logging.getLogger(__name__)

class ResultAnalyzer:
    """Analyzes experiment results and generates figures."""

    def __init__(self, results_path: Path = None):
        self.results_path = results_path or config.paths.results
        self.output_dir = config.paths.figures
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_results(self) -> pd.DataFrame:
        """Loads results from CSV."""
        if not self.results_path.exists():
            raise FileNotFoundError(f"Results file not found at {self.results_path}")
        return pd.read_csv(self.results_path)

    def generate_report(self):
        """Generates statistical report and plots."""
        df = self.load_results()
        
        # Statistical Summary
        summary = df.groupby('strategy')['vector_distance'].agg(['mean', 'var', 'std', 'count']).sort_values('mean')
        print("\n=== Statistical Summary (Vector Distance) ===")
        print(summary)
        summary.to_csv(self.output_dir / "summary_stats.csv")

        # Set plot style
        sns.set_theme(style="whitegrid")

        # 1. Bar Plot: Mean Distance by Strategy
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df, x='strategy', y='vector_distance', errorbar='sd', palette='viridis')
        ax.set_title('Mean Vector Distance by Prompt Strategy (Lower is Better)')
        ax.set_ylabel('Cosine Distance')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / "mean_distance_comparison.png")
        plt.close()

        # 2. Violin Plot / Box Plot for Distribution
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df, x='strategy', y='vector_distance', palette='viridis', inner="quartile")
        plt.title('Distribution of Vector Distances by Strategy')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / "distance_distribution.png")
        plt.close()

        logger.info(f"Analysis complete. Figures saved to {self.output_dir}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        analyzer = ResultAnalyzer()
        analyzer.generate_report()
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
