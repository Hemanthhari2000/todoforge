## Lint using ruff
.PHONY: ruff
ruff: 
	poetry run ruff check

## Format files using black
.PHONY: format
format: 
	poetry run ruff check --fix
	poetry run black .

## Run checks (ruff + test + typing)
.PHONY: check
check: 
	poetry run ruff check .
	poetry run black --check .
	poetry run dmypy run -- .

# Run all for dev
.PHONY: all-dev
all-dev: ruff format check 



