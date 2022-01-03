NAME = bobcat-miner

SHELL := /bin/bash

.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: lint tests run

build: ## Build the container
	docker build . -t $(NAME)

dev: build ## Get python interepter in the container
	docker run -v "$$(pwd)/src/bobcat":/bobcat --rm -it --env-file .env --entrypoint /bin/bash $(NAME)

run: build ## Run the container
	docker run --rm -it --env-file .env $(NAME)

quick-run: ## Run the container
	docker -v "$$(pwd)/src/bobcat":/bobcat --rm -it --env-file .env $(NAME)

tests: build ## Run the unittests
	docker run --rm -it --entrypoint='python' $(NAME) /bobcat/tests.py -v

lint: ## Run the unittests
	black --line-length 100 src
