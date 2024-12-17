
# Contributing to Todoforge

Thank you for your interest in contributing to Todoforge! 🎉 Your contributions help improve this CLI-based to-do tracker for productive developers. Whether you're fixing a bug, adding a feature, or improving documentation, your efforts are greatly appreciated.

## Table of Contents
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation](#improving-documentation)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Code Guidelines](#code-guidelines)
- [Pull Request Process](#pull-request-process)

---

## How Can I Contribute?

### Reporting Bugs
If you encounter a bug, please help us by reporting it:
1. Search existing [issues](https://github.com/username/todoforge/issues) to ensure the bug hasn’t already been reported.
2. If the issue is new, [open a new issue](https://github.com/username/todoforge/issues/new) and include:
   - A clear title.
   - Steps to reproduce the issue.
   - The expected and actual behavior.
   - Environment details (e.g., OS, Python version).

### Suggesting Features
We welcome feature requests! To propose a new feature:
1. Search [issues](https://github.com/username/todoforge/issues) to see if the idea has already been discussed.
2. [Open a feature request](https://github.com/username/todoforge/issues/new) with:
   - A detailed description of the feature.
   - Any use cases or benefits.
   - Mockups or examples (if applicable).

### Improving Documentation
Help improve our documentation by:
1. Fixing typos, grammatical errors, or outdated information.
2. Adding examples, tutorials, or FAQs.

Feel free to [open a pull request](#pull-request-process) or suggest edits directly in the documentation files.

### Contributing Code
Before submitting code:
1. Ensure it aligns with our [Code Guidelines](#code-guidelines).
2. If it's a significant change, discuss it in an issue first.
3. Add or update relevant tests for the change.

---

## Development Setup

### Prerequisites
- Python (3.12 or later)
- Poetry (for dependency management)
- Git

### Setting Up Your Environment
1. Clone the repository:
   ```bash
   git clone https://github.com/username/todoforge.git
   cd todoforge
   ```
2. Installing dependencies using Poetry:
  ```bash
    make install-dev
  ```
3. Installing pre-commit:
  ```bash
    make install-pre-commit
  ```
4. Activate the virtual environment:
  ```bash
    poetry shell

  ```
5. Run tests to ensure everything works:
  ```bash
    make test
  ```

### Running the CLI locally
Use the development version of Todoforge:
  ```bash
    poetry run tdf --help
  ```

## Code Guidelines

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.
- Use type hints wherever applicable
- Keep functions and classes modular and reusable.

### Linting and Formatting
We use `black` for formatting and `ruff` for linting:
  ```bash
    make format && make ruff
  ```
### Writing Tests
- All new features must include unit tests.
- Place tests in the tests/ directory.
- Run tests using:
  ```bash
    make test
  ```

## Pull Request Process
1. Fork the repository and create your branch:
```bash
git checkout -b feature/my-new-feature
```

2. Commit your changes with a clear message:
```bash
git commit -m "Add my new feature"
```

> Note:
> - Make sure pre commit checks are passing. If not, then resolve and try to commit again.

3. Push to your fork:
```bash
git push origin feature/my-new-feature
```

4. Open a pull request (PR) to the main branch:
- Ensure your PR includes a description of the change.
- Reference related issues in the PR description.

5. Wait for feedback and address any comments or requested changes.


