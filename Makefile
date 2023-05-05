init:
	pip install -r requirements.txt

imports:
	@isort .

data:
	@./scripts/collect_cities_and_countries_data.py
	@./scripts/collect_forenames_data.py
	@./scripts/collect_surnames_data.py

test:
	pytest --cov=src tests/

latest_tag:
	@git tag --sort=committerdate --list '[0-9]*' | tail -1

bump:
	@bumpver update $(v)
	@git push
	@git push origin `make --no-print-directory latest_tag`

build:
	@mkdir -p dist/archive
	@if [ 0 -ne `find dist -maxdepth 1 -type f | wc -l` ] ; then\
		mv dist/mimeograph* dist/archive;\
	fi
	@python -m build

publish:
	@twine upload dist/mimeograph-$(v)*

upgrade:
	@make --no-print-directory bump v=$(v)
	@make --no-print-directory build
	@make --no-print-directory publish v=`make --no-print-directory latest_tag`
