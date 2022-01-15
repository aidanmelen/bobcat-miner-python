NAME = bobcat-miner-python

SHELL := /bin/bash

.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: lint tests run

build: ## Build the container
	docker build . -t $(NAME)

dev: build ## Get python interepter in the container
	docker run -v "$$(pwd)":/bobcat_miner_python --rm -it --env-file .env --entrypoint /bin/bash $(NAME)

run: build ## Run the container
	docker run --rm -it --env-file .env $(NAME)

bobcat-autopilot: ## Run the bobcat-auotpilot
	docker run -v "$$(pwd)":/bobcat_miner_python --rm -it --env-file .env $(NAME) poetry run bobcat-autopilot

tests: build ## Run the unittests
	docker run --rm -it --entrypoint='/bobcat_miner_python/tests-entrypoint.sh' $(NAME)

lint: ## Run the unittests
	black --line-length 100 src/bobcat_miner tests
