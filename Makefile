# Makefile for Django project

MANAGE=python manage.py

.PHONY: help runserver migrate makemigrations collectstatic test shell

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

runserver: # Run the Django development server
	$(MANAGE) runserver

migrate: #Apply database migrations
	$(MANAGE) migrate

makemigrations: # Create new database migrations based on changes to models
	$(MANAGE) makemigrations

collectstatic: # Collect static files into STATIC_ROOT
	$(MANAGE) collectstatic --noinput

test: # Run tests
	$(MANAGE) test

shell: # Open the Django shell
	$(MANAGE) shell

createsuperuser: # Create a superuser
	$(MANAGE) createsuperuser

check: # Check for any errors in the project
	$(MANAGE) check

showmigrations: # Show all migrations and their status
	$(MANAGE) showmigrations

start: migrate makemigrations runserver # Migrate, collect static files, and run the server