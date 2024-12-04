check-test-requirements:
	sort-requirements --check requirements/dev.txt

check-flake8-requirements:
	sort-requirements --check requirements/flake8.txt

test:
	cd egame && python manage.py test

black-check:
	black --check --verbose -- .

isort-check:
	isort --check --verbose -- .

flake8-check:
	flake8 . --verbose --count --show-source --statistics
