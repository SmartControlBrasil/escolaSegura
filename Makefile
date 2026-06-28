.PHONY: install migrate seed run test check deploy-check collectstatic

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

migrate:
	. .venv/bin/activate && python manage.py migrate

seed:
	. .venv/bin/activate && python manage.py seed_base

run:
	. .venv/bin/activate && python manage.py runserver

test:
	. .venv/bin/activate && python manage.py test

check:
	. .venv/bin/activate && python manage.py check

deploy-check:
	. .venv/bin/activate && DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py check --deploy

collectstatic:
	. .venv/bin/activate && python manage.py collectstatic --noinput
