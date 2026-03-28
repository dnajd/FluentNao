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

ssh-setup: ## generate PEM key and copy to NAO for passwordless SSH
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	@if [ ! -f ~/.ssh/id_nao ]; then \
		echo "Generating PEM-format RSA key for NAO..."; \
		ssh-keygen -t rsa -m pem -f ~/.ssh/id_nao -N "" -C "fluentnao-docker"; \
	else \
		echo "Key ~/.ssh/id_nao already exists, skipping generation"; \
	fi
	@echo "Copying key to NAO (you will be prompted for the NAO password)..."
	ssh-copy-id -i ~/.ssh/id_nao nao@$$NAO_IP
	@echo "Fixing permissions on NAO (you may be prompted for the password again)..."
	ssh -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostkeyAlgorithms=+ssh-rsa -i ~/.ssh/id_nao nao@$$NAO_IP "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
	@echo ""
	@echo "Done! Test with: ssh nao"
	@echo ""
	@echo "Add this to ~/.ssh/config if you haven't already:"
	@echo ""
	@echo "Host nao"
	@echo "    HostName $$NAO_IP"
	@echo "    User nao"
	@echo "    IdentityFile ~/.ssh/id_nao"
	@echo "    PubkeyAcceptedAlgorithms +ssh-rsa"
	@echo "    HostkeyAlgorithms +ssh-rsa"

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
	docker compose run --service-ports -e NAO_IP=$$NAO_IP fluentnao sh -c "./bootstrap.sh"

serve: ## run http server (non-interactive)
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	docker compose run --service-ports -e NAO_IP=$$NAO_IP fluentnao sh -c "./bootstrap_server.sh"