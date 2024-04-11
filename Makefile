export POSTGRES_DATABASE_URL=postgresql+psycopg2://postgres:evs!123@localhost:5432/evs


install_poetry:
	curl -sSL https://install.python-poetry.org | python3 -

setup_env:
	poetry install

create_changelog:
	touch CHANGELOG.md

update_version:
	poetry version patch

run_tests:
	poetry run pytest

run_locally:
	# flake8 app
	poetry run uvicorn app.main:app --reload

build_db:
	docker build -t mypostgres -f Dockerfile.postgres .

run_db:
	if [ -n "`docker ps -a | grep 'mypostgres.*Exited'`" ]; then \
		docker start mypostgres; \
	else \
		docker run -d -p 5432:5432 --name mypostgres -v dbdata:/var/lib/postgresql/data mypostgres; \
	fi

db_init:
	poetry run alembic init alembic

db_migration:
	poetry run alembic revision --autogenerate -m "migration message"

db_upgrade:
	poetry run alembic upgrade head

db_downgrade:
	poetry run alembic downgrade -1

.PHONY: install_poetry setup_env run_db run_locally migrate db_init create_changelog update_version