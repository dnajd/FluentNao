.DEFAULT_GOAL := help
BLUE := $(shell tput setaf 4)
RESET := $(shell tput sgr0)

help:
	@printf "\n# Help\n\n"
	@grep -E '^[^ .]+: .*?## .*$$' $(MAKEFILE_LIST) \
		| awk '\
			BEGIN { FS = ": .*##" };\
			{ gsub(";", "\n\t\t      ") }; \
			{ printf "%-20s$(RESET) %s\n", $$1, $$2 }'
	@printf "\n"

init: ## build the docker image;
	docker compose build

bash: ## bash prompt
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	docker compose run -e NAO_IP=$$NAO_IP fluentnao bash

up: ## up
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	docker compose run -e NAO_IP=$$NAO_IP fluentnao sh -c "./bootstrap.sh"