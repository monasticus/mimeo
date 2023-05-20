init:
	@python -m pip install pip-tools
	@pip-compile --extra dev pyproject.toml
	@pip install -r requirements.txt
	@pip install -e .

imports:
	@isort .
	@isort -a "from __future__ import annotations" src scripts

data:
	@./scripts/collect_cities_and_countries_data.py
	@./scripts/collect_currencies_data.py
	@./scripts/collect_forenames_data.py
	@./scripts/collect_surnames_data.py

test:
	pytest --cov=src tests/

latest_tag:
	@git tag --sort=committerdate --list '[0-9]*' | tail -1

build:
	@mkdir -p dist/archive
	@if [ 0 -ne `find dist -maxdepth 1 -type f | wc -l` ] ; then\
		mv dist/mimeograph* dist/archive;\
	fi
	@python -m build

publish:
	@twine upload dist/mimeograph-$(v)*

build_and_publish:
	@make --no-print-directory build
	@make --no-print-directory publish v=`make --no-print-directory latest_tag`

check_new_linters:
	python -m pip install --upgrade ruff
	@./meta/linters/look_for_new_linters.py

