# Install dependencies
.PHONY: install
install:
	poetry install --without dev 

# Install dev-dependencies
.PHONY: install-dev
install-dev: install
	poetry install --only dev

# Install pre commit hooks
.PHONY: install-pre-commit
install-pre-commit: 
	poetry run python -m pip install pre-commit
	poetry run pre-commit install
	poetry run pre-commit run --all-files

## Lint using ruff
.PHONY: ruff
ruff: 
	poetry run ruff check --fix

## Format files using black
.PHONY: format
format: 
	poetry run ruff check --fix
	poetry run black .

# Run checks (ruff + test + typing)
.PHONY: check
check: 
	poetry run ruff check .
	poetry run black --check .
	poetry run dmypy run -- .

# Run tests
.PHONY: test
test:
	poetry run coverage run -m pytest -s
	poetry run coverage report

# Run all for dev
.PHONY: all-dev
all-dev: ruff format check test



