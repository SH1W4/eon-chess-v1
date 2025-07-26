.PHONY: setup test lint build up down clean help

help: ## Mostra esta mensagem de ajuda
	@echo 'Uso: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Configura o ambiente de desenvolvimento
	npm install
	pip install -r requirements.txt
	go mod download

test: ## Executa todos os testes
	npm test
	python -m pytest
	go test ./...

lint: ## Executa linters e formatadores
	npm run lint
	black .
	gofmt -w .

build: ## Constrói o projeto para produção
	npm run build
	go build -o bin/aeon cmd/main.go

up: ## Inicia todos os serviços em containers
	docker-compose up -d

down: ## Para todos os serviços
	docker-compose down

clean: ## Limpa arquivos temporários e caches
	rm -rf node_modules
	rm -rf dist
	rm -rf __pycache__
	rm -rf .pytest_cache
	go clean

# Define o target padrão
.DEFAULT_GOAL := help
