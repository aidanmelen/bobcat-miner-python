NAME = bobcat-miner-python
VERSION = $(shell poetry version -s)

SHELL := /bin/bash

.PHONY: help all build dev run bobcat-autopilot tests lint

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: build-all lint tests run

build: ## Build
	docker build . -t bobcat
	docker build . -t $(NAME)-test --target test
	docker-compose build

up: ## Spin up local dev stack
	docker-compose up -d --remove-orphans

dev: up ## Build and run dev container
	docker-compose exec $(NAME)-dev poetry run /bin/bash

dev-fancy-awesome-bobcat: up ## Build and run dev container
	docker-compose exec fancy-awesome-bobcat /bin/bash

down: ## Spin down local dev stack
	docker-compose down

lint: ## Lint with black
	docker run --rm --volume "$$(pwd)":/src --workdir /src pyfound/black:latest_release black --line-length 100 . 

test: ## Build and run dev container
	docker run --rm -it -v "$$(pwd)":/app $(NAME)-test

tests: lint test ## Lint and Test

run: ## Run the 'bobcat autopilot' in a container
	docker run --rm -it -v "$$(pwd)":/app --env-file .env bobcat autopilot

# lint: ## Run the linter
# 	black --line-length 100 .

# test: ## Run the unittests
# 	docker run -v "$$(pwd)":/app --rm -it $(NAME)-dev python -m unittest discover -s tests -v

release: all  ## Push tags and trigger Github Actions release.
	git tag $(VERSION)
	git push --tags

clean: ## Remove Python cache files.
	@rm -rf build dist .eggs *.egg-info .venv requirements.txt
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +