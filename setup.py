from setuptools import find_packages, setup

setup(
    name="prompt_engineering_analysis",
    version="0.1.0",
    description="Analysis of prompt engineering effectiveness using Logic Puzzles",
    author="Code Agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "ollama",
        "numpy<2.0.0",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "sentence-transformers",
        "pyyaml",
    ],
)
