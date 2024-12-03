PYTHON_VERSION = 3.11
PIP = pip install --upgrade pip

check-test-requirements:
	$(PIP)
	pip install sort-requirements
	sort-requirements --check requirements/prod.txt
	sort-requirements --check requirements/test.txt

check-flake8-requirements:
	$(PIP)
	pip install sort-requirements
	sort-requirements --check requirements/flake8.txt

install-prod:
	$(PIP)
	pip install -r requirements/prod.txt

install-test:
	$(PIP)
	pip install -r requirements/test.txt

install-lint:
	$(PIP)
	pip install -r requirements/flake8.txt

install-isort:
	$(PIP)
	pip install isort

test: install-prod install-test
	cd egame && python manage.py test

black-check:
	black --check --verbose -- .

isort-check: install-isort
	isort --check --verbose -- .

flake8-check: install-lint
	flake8 . --verbose --count --show-source --statistics