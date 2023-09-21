.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= ./docker-compose.yml
SOURCE_FILES ?= server

POETRY_EXPORT_WITHOUT_INDEXES ?= true
POETRY_EXPORT_OUTPUT = requirements.txt
POETRY_VERSION = 1.6.0
POETRY ?= $(HOME)/.poetry/bin

MIGRATIONS_DB_CONFIG = server/alembic.ini

.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install-packages
install-packages:
	poetry install

.PHONY: update
update:
	poetry update -v

.PHONY: service
service:
	poetry run python server/main.py

.PHONY: docker-build
docker-build:
	@docker build \
		--tag=iban-checked-backend \
		--file=./Dockerfile \
		--build-arg BUILD_RELEASE=dev \
		.

.PHONY: docker-prune
docker-prune:
	docker container prune -f
	docker volume prune -f

.PHONY: docker-up
docker-up:
	docker-compose -f $(COMPOSE_FILE) --env-file=.env up -d
	docker-compose -f $(COMPOSE_FILE) ps

.PHONY: docker-upnd
docker-upnd:
	docker-compose -f $(COMPOSE_FILE) --env-file=.env up

.PHONY: docker-down
docker-down:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: docker-restart
docker-restart:
	make docker-down
	make docker-up

.PHONY: docker-prune
docker-prune:
	docker container prune -f
	docker volume prune -f

.PHONY: migrate
migrate:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) upgrade head

.PHONY: migrations
migrations:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) revision --autogenerate --message auto

.PHONY: alembic-history
alembic-history:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) history

.PHONY: alembic-merge-heads
alembic-merge-heads:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) merge heads

.PHONY: alembic-downgrade-local
alembic-downgrade-local:
	docker-compose exec backend alembic --config $(MIGRATIONS_DB_CONFIG) downgrade -1

.PHONY: tests
tests:
	docker-compose --env-file .env -f $(COMPOSE_FILE) exec backend pytest tests/.

.PHONY: isort
isort:
	isort ./$(SOURCE_FILES)

.PHONY: lint-isort
lint-isort:
	isort --check-only --diff ./$(SOURCE_FILES)

.PHONY: lint-flake
lint-flake:
	flake8 ./$(SOURCE_FILES) --append-config ./.flake8

.PHONY: lint
lint: lint-isort lint-flake
