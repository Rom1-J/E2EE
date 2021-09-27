VIRTUAL_ENV := venv
PYTHON_PATH := $(VIRTUAL_ENV)/bin/python

MANAGE_PY := DJANGO_READ_DOT_ENV_FILE=True $(PYTHON_PATH) manage.py

TESTS := chat/pages/tests/ chat/users/tests/ chat/guilds/tests/

#######################
# Dev
#######################
.PHONY: run
run:
	$(MANAGE_PY) runserver_plus 0.0.0.0:8000

.PHONY: gulp
gulp:
	DJANGO_READ_DOT_ENV_FILE=True npm run dev

.PHONY: console
console: shell

.PHONY: shell
shell:
	$(MANAGE_PY) shell

#######################
# Database
#######################
.PHONY: migrations
migrations:
	$(MANAGE_PY) makemigrations

.PHONY: migrate
migrate:
	$(MANAGE_PY) migrate

#######################
# Style
#######################
.PHONY: lint
lint:
	$(PYTHON_PATH) -m pylint chat --load-plugins=pylint_django --django-settings-module=config.settings.local $(addprefix -d duplicate-code , $(TESTS))

.PHONY: black
black:
	$(PYTHON_PATH) -m black chat --line-length=79
	$(PYTHON_PATH) -m black config --line-length=79

.PHONY: type
type:
	$(PYTHON_PATH) -m mypy chat

.PHONY: style
style: black type lint