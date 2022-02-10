NAME = bobcat-miner-python
VERSION = $(shell poetry version -s)

SHELL := /bin/bash

.PHONY: help all

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: build tests run

# linux/amd64
build: ## Build lint and test images and build Docker Compose services
	docker build -f Dockerfile.dev . -t $(NAME)-lint --target lint
	docker build -f Dockerfile.dev . -t $(NAME)-test --target test
	docker-compose build

build-release: ## Build multi-platform release images
	docker buildx build . -t bobcat --platform linux/amd64,linux/arm/v7

up: ## Spin up local development stack
	docker-compose up -d

dev: up ## Attach to the bobcat-miner-python dev container
	docker-compose exec $(NAME)-dev poetry run /bin/bash

dev-bobcat: up ## Attach to the fancy-awesome-bobcat dev container
	docker-compose exec fancy-awesome-bobcat /bin/bash

down: ## Spin down local dev services
	docker-compose down

lint: ## Lint with black
	docker run --rm -it -v "$$(pwd)":/app $(NAME)-lint

test: ## Run unittests
	docker run --rm -it -v "$$(pwd)":/app $(NAME)-test

tests: lint test ## Lint and Test

run: ## Run the 'bobcat autopilot' in a container
	docker run --rm -it --env-file .env bobcat autopilot

release: tests  ## Push tags and trigger Github Actions release.
	git tag $(VERSION)
	git push --tags

clean: ## Remove Python cache files.
	@rm -rf build dist .eggs *.egg-info .venv requirements.txt
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +