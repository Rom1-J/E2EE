VIRTUAL_ENV := venv
PYTHON_PATH := $(VIRTUAL_ENV)/bin/python

MANAGE_PY := DJANGO_READ_DOT_ENV_FILE=True $(PYTHON_PATH) manage.py


run:
	$(MANAGE_PY) runserver_plus 0.0.0.0:8000

gulp:
	DJANGO_READ_DOT_ENV_FILE=True npm run dev

migrate:
	$(MANAGE_PY) migrate
