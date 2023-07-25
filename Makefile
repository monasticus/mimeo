install:
	@pip install poetry
	@poetry install

update:
	poetry update

imports:
	@poetry run isort .
	@poetry run isort -a "from __future__ import annotations" src scripts

lint:
	@poetry run ruff .

lint_fix:
	@poetry run ruff . --fix

test:
	poetry run pytest --cov=src/mimeo tests/

data:
	@./scripts/collect_cities_and_countries_data.py
	@./scripts/collect_currencies_data.py
	@./scripts/collect_forenames_data.py
	@./scripts/collect_surnames_data.py

latest_tag:
	@git tag --sort=committerdate --list '[0-9]*' | tail -1

build:
	@mkdir -p dist/archive
	@if [ 0 -ne `find dist -maxdepth 1 -type f | wc -l` ] ; then\
		mv dist/mimeograph* dist/archive;\
	fi
	@poetry build

publish:
	@poetry publish

build_and_publish:
	@make --no-print-directory build
	@make --no-print-directory publish

linters:
	poetry update ruff
	@./meta/linters/look_for_new_linters.py

update_linters:
	@poetry run ruff linter --format=json > ./meta/linters/linters.json

