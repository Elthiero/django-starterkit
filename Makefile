# Makefile
.PHONY: run migrate migrations shell static superuser

run:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

shell:
	python3 manage.py shell_plus 2>/dev/null || python3 manage.py shell

static:
	python3 manage.py collectstatic --noinput

superuser:
	python3 manage.py createsuperuser

test:
	python3 manage.py test --verbosity=2

freeze:
	pip freeze > requirements.txt

fresh:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	python3 manage.py makemigrations
	python3 manage.py migrate