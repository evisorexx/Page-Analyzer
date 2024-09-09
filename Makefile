PORT ?= 5000

install:
	poetry install

build:
	./build.sh

db_restore:
	poetry run pg_restore -d padb padb.dump
	
lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app run --port $(PORT)

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app