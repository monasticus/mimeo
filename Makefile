init:
	pip install -r requirements.txt

imports:
	isort .

test:
	pytest --cov=src tests/

get_data:
	python scripts/get_cities_and_countries_data.py
