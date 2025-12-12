"""
Module for generating logic puzzle datasets (Syllogisms).
"""
import json
import random
from pathlib import Path


class SyllogismGenerator:
    """Generates syllogism problems with ground truth."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        
        # Simple knowledge base for template filling
        self.subjects: list[str] = ["cats", "dogs", "birds", "fish", "programmers", "philosophers"]
        self.middle_terms: list[str] = ["mammals", "animals", "living things", "logic users", "humans", "mortals"]
        self.predicates: list[str] = ["breathing", "warm-blooded", "capable of thought", "destined to die", "part of nature"]

    def generate_valid_syllogism(self) -> dict[str, str]:
        """Generates a valid syllogism (Yes answer)."""
        s = random.choice(self.subjects)
        m = random.choice(self.middle_terms)
        p = random.choice(self.predicates)
        
        # Valid: All S are M. All M are P. -> All S are P.
        question = f"Premise 1: All {s} are {m}.\nPremise 2: All {m} are {p}.\nQuestion: Are all {s} {p}?"
        return {
            "question": question,
            "answer": "Yes, because all " + s + " are " + m + " and all " + m + " are " + p + ".",
            "label": "Yes"
        }

    def generate_invalid_syllogism(self) -> dict[str, str]:
        """Generates an invalid/indeterminate syllogism (No answer)."""
        s = random.choice(self.subjects)
        m = random.choice(self.middle_terms)
        p = random.choice(self.predicates)
        
        # Invalid: All S are M. Some P are M. -> All S are P? (Undetermined/No)
        question = f"Premise 1: All {s} are {m}.\nPremise 2: Some {p} are {m}.\nQuestion: Are all {s} {p}?"
        return {
            "question": question,
            "answer": "No, it does not follow logically.",
            "label": "No"
        }

    def generate_dataset(self, size: int = 20) -> list[dict[str, str]]:
        """Generates a balanced dataset of valid and invalid syllogisms."""
        dataset: list[dict[str, str]] = []
        for _ in range(size // 2):
            dataset.append(self.generate_valid_syllogism())
            dataset.append(self.generate_invalid_syllogism())
        
        random.shuffle(dataset)
        return dataset

    def save_dataset(self, dataset: list[dict[str, str]], filepath: Path) -> None:
        """Saves the dataset to a JSON file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(dataset, f, indent=2)

if __name__ == "__main__":
    # Test generation
    gen = SyllogismGenerator()
    data = gen.generate_dataset(5)
    print(json.dumps(data, indent=2))
