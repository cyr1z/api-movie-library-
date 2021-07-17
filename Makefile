# import config.
# You can change the default config with `make cnf="config_special.env" build`
cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# default: build

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(APP_NAME):$(VERSION) -t $(APP_NAME):latest .

build-nc: ## Build the container without caching
	docker build --no-cache -t $(APP_NAME):$(VERSION) -t $(APP_NAME):latest .

up: ## Up container from registry image
	docker-compose -f docker-compose.yml up -d

dev-up: ## Run container on port configured in `.env`
	black .
	docker-compose -f docker-compose.dev.yml  up --build

run: ##  Run container on port configured in `.env` with -d (background mode)
	docker run -d -t --rm  --env-file=.env  --name="$(APP_NAME)" $(APP_NAME)

rm: ## Stop and remove a running container
	docker rm $(APP_NAME) || true

stop: ## Stop and remove a running container
	docker-compose --env-file .env stop

dev-stop: ## Stop and remove a running container
	docker-compose --env-file .env -f docker-compose.dev.yml stop

logs: ## view logs
	docker logs $(APP_NAME)

log-tail: ## tail log
	docker exec -i $(APP_NAME) tail -f $(LOG_PATH)

clean: ## Cleaning up old container images and cache files
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	docker-compose down -v
	# docker rmi $(docker images -f "dangling=true"-q)

flake: ## Run flake8 linters
	flake8 -v app

pylint: ## Run Pylint linter
	pylint app

test: ## Run tests
	docker exec $(APP_NAME) python -i -m pytest -q /tests/unit/ -p no:warnings

test-last-failed: ## Run last failed tests only
	docker exec $(APP_NAME) python -m pytest -q /tests/unit/ --lf

test-dev: ## Run tests with covarege
	python -m pytest -v --cov=src --cov-report term-missing ./tests/unit/ --cov ./src/app

kill: ## Kill a running container
	docker kill $(APP_NAME)

pip-freeze: ## freezing dependencies
	pip freeze > requirements.txt

release: build-nc publish ## Make a release by building and publishing the `{version}` and `latest` tagged containers to registry.

# Docker publish
publish: repo-login publish-latest publish-version ## Publish the `{version}` and `latest` tagged containers to registry.

publish-latest: tag-latest ## Publish the `latest` tagged container to ECR
	@echo 'publish latest to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO):latest

publish-version: tag-version ## Publish the `{version}` tagged container to ECR
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO):$(VERSION)

## Docker tagging
tag: tag-latest tag-version ## Generate container tags for the `{version}` ans `latest` tags

tag-latest: ## Generate container `{version}` tag
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO):latest

tag-version: ## Generate container `latest` tag
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO):$(VERSION)

shell: ## run bash in container
	docker exec -i -t $(APP_NAME) bash

sh: ## run sh in container
	docker exec -i -t $(APP_NAME) sh

#ask_password:
#	@$(eval PASSWORD=$(shell stty -echo; read -p "Password: " pwd; stty echo; echo $$pwd))
#
## login to REGISTRY
#repo-login: ask_password ## login to repo
#	 docker login --username $(DOCKER_USER) --password $(PASSWORD) $(DOCKER_REGISTRY)

# login to registry
repo-login: ## login to repo
	docker login --username $(DOCKER_USER) --password $(DOCKER_PASSWORD) $(DOCKER_REGISTRY)

pull: ## pull latest docker image
	docker pull $(DOCKER_REPO)

version: ## Output the current version
	@echo $(VERSION)

#send-link:
#	./infra/tg.sh 'https://$(DOCKER_REPO)/v2/$(APP_NAME)/manifests/$(VERSION)/'
#	./infra/tg.sh 'docker pull $(DOCKER_REPO)'

psql: ## database console
	docker exec -it db-$(APP_NAME) psql --username=${POSTGRES_USER} --dbname=${POSTGRES_DB}

db-bash: ## bash in database container
	docker exec -it db-$(APP_NAME)  bash

migrate: ## database migrate
	docker exec -i $(APP_NAME)  flask db migrate

db-upgrade: ## database upgrade
	docker exec -i $(APP_NAME)  flask db upgrade

flask-shell: ## flask shell
	docker exec -i $(APP_NAME)  flask shell
