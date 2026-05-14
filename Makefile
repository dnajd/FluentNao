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
	UID=$$(id -u) GID=$$(id -g) docker compose build --build-arg USER_ID=$$(id -u) --build-arg GROUP_ID=$$(id -g)
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
	UID=$$(id -u) GID=$$(id -g) docker compose run -e NAO_IP=$$NAO_IP fluentnao bash

up: ## up
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	UID=$$(id -u) GID=$$(id -g) docker compose run --service-ports -e NAO_IP=$$NAO_IP fluentnao sh -c "./bootstrap.sh"

serve: ## run http server (non-interactive)
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	UID=$$(id -u) GID=$$(id -g) docker compose run --service-ports -e NAO_IP=$$NAO_IP fluentnao sh -c "./bootstrap_server.sh"

boot: ## start server and perform initial robot setup
	@$(MAKE) serve &
	@echo "Waiting for server to start..."
	@sleep 8
	@$(MAKE) health
	@curl -s -X POST http://localhost:5050/exec -d "nao.say('ready')"
	@echo "Robot is ready."

health: ## check server and robot status
	@curl -s http://localhost:5050/health
	@echo ""
	@curl -s -X POST http://localhost:5050/exec -d "import time; result = {'battery': nao.sensors.battery_level(), 'stiff': any(nao.joint_angles('Body', True)), 'temp': nao.sensors.hottest_joint(), 'time': time.strftime('%H:%M')}"
	@echo ""

transcribe: ## transcribe the latest audio recording using Whisper
	@ls -t data/audio/*.wav | head -n 1 | xargs -I {} ~/.local/bin/whisper {} --model base --language en --output_format txt --output_dir data/audio/
	@ls -t data/audio/*.txt | head -n 1 | xargs -I {} cat {}

serve-log: stop ## restart server with request logging visible
	@if [ -z "$$NAO_IP" ]; then \
		echo "ERROR: provide NAO_IP environment variable"; \
		exit 1; \
	else \
        echo "NAO IP: $$NAO_IP"; \
    fi
	UID=$$(id -u) GID=$$(id -g) docker compose run --service-ports -e NAO_IP=$$NAO_IP -e FLUENTNAO_LOG=1 fluentnao sh -c "./bootstrap_server.sh"

monitor: ## watch Claude sessions and push events to NAO server (runs on host, not in Docker)
	@echo "Starting session monitor (polls every 2m, NAO_SERVER=$(or $(NAO_SERVER),http://localhost:5050))..."
	NAO_SERVER=$(or $(NAO_SERVER),http://localhost:5050) python3 scripts/session_monitor.py

stop: ## stop any running fluentnao containers
	@docker compose down 2>/dev/null || true
	@docker ps -q --filter ancestor=fluentnao:dev | xargs -r docker stop 2>/dev/null || true
	@echo "Stopped"