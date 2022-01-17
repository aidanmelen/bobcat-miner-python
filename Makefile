NAME = bobcat-miner-python

SHELL := /bin/bash

.PHONY: help all build dev run bobcat-autopilot tests lint

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: lint tests run

build: ## Build the container
	docker build . -t $(NAME)

dev: ## Get python interepter in the container
	docker run -v "$$(pwd)":/bobcat_miner_python --rm -it --entrypoint=/bobcat_miner_python/entrypoint-dev.sh --env-file .env $(NAME)

run: ## Run the container
	docker run --rm -it --env-file .env $(NAME)

bobcat-autopilot: ## Run the bobcat-autopilot
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --env-file .env $(NAME) autopilot

tests: ## Run the unittests
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)

tests-all: ## Run the unittests
	docker build . --build-arg PYTHON_VERSION=3.8 -t $(NAME)
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)
	docker build . --build-arg PYTHON_VERSION=3.9 -t $(NAME)
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)
	docker build . --build-arg PYTHON_VERSION=3.10 -t $(NAME)
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)

lint: ## Run the linter
	black --line-length 100 .