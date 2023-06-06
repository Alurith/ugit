pkg_src = ugit
tests_src = tests
all_src = $(pkg_src) $(tests_src)

mypy_base = mypy --show-error-codes --explicit-package-bases
mypy = $(mypy_base) $(all_src)
test = pytest $(tests_src) --cov=ugit

# Run formatting, static checks, and tests
all: format mypy test

## Format the soruce cde (isort, black, ruff)
format:
	isort $(all_src)
	black $(all_src)
	ruff --fix $(all_src)

lint:
	black --check --diff $(all_src)
	ruff $(all_src) 

## Run tests
test:
	$(test)

mypy:
	$(mypy)

## Run all CI validation steps
ci: lint mypy test
