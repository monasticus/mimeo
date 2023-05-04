init:
	pip install -r requirements.txt

imports:
	@isort .

data:
	@./scripts/collect_cities_and_countries_data.py
	@./scripts/collect_forenames_data.py
	@./scripts/collect_surnames_data.py

test:
	pytest --cov=src --cov-report term-missing:skip-covered tests/

bump:
	@bumpver update $(v)
	@git push
	@git push origin `git tag --sort=committerdate --list '[0-9]*' | tail -1`

build:
	@mkdir -p dist/archive
	@if [ 0 -ne `find dist -maxdepth 1 -type f | wc -l` ] ; then\
		mv dist/mimeograph* dist/archive;\
	fi
	@python -m build

publish:
	@twine upload dist/mimeograph*

upgrade: bump build publish
