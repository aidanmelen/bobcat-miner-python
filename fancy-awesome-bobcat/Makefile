NAME = fancy-awesome-bobcat

SHELL := /bin/bash

.PHONY: help all build dev

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

all: lint tests run

build: ## Build the container
	docker build . -t $(NAME)

dev: ## Get python interepter in the container
	docker run --rm -it -p 80:80 -v "$$(pwd)/src/bobcat":/bobcat --entrypoint /bin/bash $(NAME)

run: ## Run the container
	docker run --rm -d -p 80:80 $(NAME)