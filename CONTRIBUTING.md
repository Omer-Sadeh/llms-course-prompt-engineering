# Contributing Guide

Thank you for your interest in contributing to the Prompt Engineering Analysis Project!

## Getting Started

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/prompt-engineering-analysis.git
    cd prompt-engineering-analysis
    ```

2.  **Set up the environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Install pre-commit hooks**:
    ```bash
    pip install pre-commit
    pre-commit install
    ```

## Development Workflow

1.  Create a new branch for your feature or fix: `git checkout -b feature/my-new-feature`.
2.  Make your changes.
3.  Run tests: `pytest`.
4.  Run linting: `ruff check .`
5.  Commit your changes.
6.  Push to the branch: `git push origin feature/my-new-feature`.
7.  Submit a pull request.

## Code Style

-   We use **Black** for code formatting.
-   We use **Ruff** for linting.
-   Follow strict typing hints where possible.
-   Docstrings are mandatory for all public functions and classes.

## Testing

-   All new features must include unit tests.
-   We aim for >80% test coverage.
-   Run coverage checks with `pytest --cov=src tests/`.
