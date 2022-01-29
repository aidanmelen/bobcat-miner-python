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
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-dev.sh --env-file .env $(NAME)

run: ## Run the container
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --env-file .env $(NAME)

bobcat-ping: ## Run the bobcat-autopilot
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --env-file .env $(NAME) ping

bobcat-autopilot: ## Run the bobcat-autopilot
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --env-file .env $(NAME) autopilot

tests-py3.8: ## Run the unittests on python3.8
	docker build . --build-arg PYTHON_VERSION=3.8 -t $(NAME)-3.8
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.8

tests-py3.9: ## Run the unittests on python3.9
	docker build . --build-arg PYTHON_VERSION=3.9 -t $(NAME)-3.9
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.9

tests-py3.10: ## Run the unittests on python3.10
	docker build . --build-arg PYTHON_VERSION=3.10 -t $(NAME)-3.10
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.10

quick-tests: ## Run the unittests on python3.10
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.8
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.9
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.10

quick-test: ## Run the unittests on python3.10
	docker run --rm -it -v "$$(pwd)":/bobcat_miner_python --entrypoint=/bobcat_miner_python/entrypoint-tests.sh $(NAME)-3.10

tests: tests-py3.8 tests-py3.9 tests-py3.10	## Run the unittests

lint: ## Run the linter
	black --line-length 100 .

release: ## publish pypi and dockerhub
	poetry build
	poetry publish
	docker push $(NAME)-3.10 aidanmelen/bobcat:latest