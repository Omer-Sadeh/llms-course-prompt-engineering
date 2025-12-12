"""
Metrics module for calculating vector distances between texts.
"""
import logging
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances

logger = logging.getLogger(__name__)

class SimilarityEvaluator:
    """Evaluates text similarity using vector embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the evaluator with a specific Sentence Transformer model.
        
        Args:
            model_name: The name of the model to load from Hugging Face Hub.
        """
        try:
            logger.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Failed to load embedding model {model_name}: {e}")
            raise

    def calculate_distance(self, text1: str, text2: str) -> float:
        """
        Calculates the cosine distance between two texts.
        
        Args:
            text1: First text string.
            text2: Second text string.
            
        Returns:
            float: Cosine distance (0 to 2, usually 0 to 1 for these embeddings).
                   0 means identical, 1 means dissimilar.
        """
        if not text1 or not text2:
            logger.warning("Empty text provided for distance calculation.")
            return 1.0 # Max distance for failure safety

        embeddings = self.model.encode([text1, text2])
        # cosine_distances returns a matrix. We want the distance between [0] and [1].
        # dist matrix: [[0, d], [d, 0]]
        dist = cosine_distances([embeddings[0]], [embeddings[1]])[0][0]
        return float(dist)

    def calculate_batch_distances(self, predictions: List[str], references: List[str]) -> List[float]:
        """Calculates distances for a batch of pairs."""
        if len(predictions) != len(references):
            raise ValueError("Predictions and references must have the same length.")
            
        distances = []
        for pred, ref in zip(predictions, references):
            distances.append(self.calculate_distance(pred, ref))
            
        return distances
