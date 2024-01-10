include docker/.env
compose_file := $(COMPOSE_FILE)
project_name := $(PROJECT_NAME)

help: ## ヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ## 開発環境構築
	cp python/.env.example python/.env
	make destroy
	docker compose -f $(compose_file) -p $(project_name) build --no-cache
	docker compose -f $(compose_file) -p $(project_name) down --volumes
	docker compose -f $(compose_file) -p $(project_name) up -d
	./docker/wait-for-db.sh
	docker compose -f $(compose_file) -p $(project_name) exec -T db mysql -psecret < docker/setup.dev.sql
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv install --dev
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv run alembic upgrade head

up: ## 開発環境up
	docker compose -f $(compose_file) -p $(project_name) up -d

down: ## 開発環境down
	docker compose -f $(compose_file) -p $(project_name) down

destroy: ## 開発環境削除
	make down
	docker network ls -qf name=$(project_name) | xargs docker network rm
	docker container ls -a -qf name=$(project_name) | xargs docker container rm
	docker volume ls -qf name=$(project_name) | xargs docker volume rm

shell: ## shellに入る
	docker compose -f $(compose_file) -p $(project_name) exec -it python bash


format: ## コードフォーマット
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv run isort .
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv run black .
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv run flake8 .
	docker compose -f $(compose_file) -p $(project_name) exec -it python pipenv run mypy .

push: ## push
# make format
	git switch main
	git pull origin main
	git add .
	git commit -m "Commit at $$(date +'%Y-%m-%d %H:%M:%S')"
	git push origin main
