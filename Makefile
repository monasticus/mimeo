init:
	pip install -r requirements.txt

imports:
	isort .

test:
	pytest tests/

bump_major:
	bumpver update --major

bump_minor:
	bumpver update --minor

bump_path:
	bumpver update --patch
