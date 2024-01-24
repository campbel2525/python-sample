include docker/.env
pf := $(COMPOSE_FILE)
pn := $(PROJECT_NAME)

help: ## ヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## 開発環境構築(ビルド)
	make destroy
	docker compose -f $(pf) -p $(pn) build --no-cache
	docker compose -f $(pf) -p $(pn) down --volumes
	docker compose -f $(pf) -p $(pn) up -d
	./docker/wait-for-db.sh
	docker compose -f $(pf) -p $(pn) exec -T db mysql -psecret < docker/setup.dev.sql
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv install --dev
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run alembic upgrade head

init: ## 開発環境構築
	cp fastapi/.env.example fastapi/.env
	cp streamlit/.env.example streamlit/.env
	cp scientist/.env.example scientist/.env
	make build

up: ## 開発環境up
	docker compose -f $(pf) -p $(pn) up -d

down: ## 開発環境down
	docker compose -f $(pf) -p $(pn) down

destroy: ## 開発環境削除
	make down
	docker network ls -qf name=$(pn) | xargs docker network rm
	docker container ls -a -qf name=$(pn) | xargs docker container rm
	docker volume ls -qf name=$(pn) | xargs docker volume rm

reset:
# dbのマイグレーションをリセットして良い場合のみ実行
# マイグレーションをリセットしない場合は、コマンドを変更すること
	rm -rf database/migrations/versions/*
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run python app/console/commands/drop_all_tables.py
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run alembic revision --autogenerate -m 'comment'
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run alembic upgrade head
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run python app/console/commands/seeds.py

fastapi-shell: ## shellに入る
	docker compose -f $(pf) -p $(pn) exec -it fastapi bash

streamlit-shell: ## shellに入る
	docker compose -f $(pf) -p $(pn) exec -it streamlit bash

scientist-shell: ## shellに入る
	docker compose -f $(pf) -p $(pn) exec -it scientist bash

check: ## コードフォーマット
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run isort .
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run black .
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run flake8 .
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run mypy .elete-log: ## pythonのログを表示

	docker compose -f $(pf) -p $(pn) exec -it streamlit pipenv run isort .
	docker compose -f $(pf) -p $(pn) exec -it streamlit pipenv run black .
	docker compose -f $(pf) -p $(pn) exec -it streamlit pipenv run flake8 .
	docker compose -f $(pf) -p $(pn) exec -it streamlit pipenv run mypy .elete-log: ## pythonのログを表示

	docker compose -f $(pf) -p $(pn) exec -it scientist pipenv run isort .
	docker compose -f $(pf) -p $(pn) exec -it scientist pipenv run black .
	docker compose -f $(pf) -p $(pn) exec -it scientist pipenv run flake8 .
	docker compose -f $(pf) -p $(pn) exec -it scientist pipenv run mypy .elete-log: ## pythonのログを表示

# rm -rf fastapi/log/fastapi.log
# rm -rf fastapi/log/sqlalchemy.log

fastapi-run: ## サーバー起動
	docker compose -f $(pf) -p $(pn) exec -it fastapi pipenv run uvicorn main:app --host 0.0.0.0 --reload --port 8000

streamlit-run: ## サーバー起動
	docker compose -f $(pf) -p $(pn) exec -it streamlit pipenv run streamlit run app/main.py --server.port 8001

push: ## push
# make format
	git switch main
	git pull origin main
	git add .
	git commit -m "Commit at $$(date +'%Y-%m-%d %H:%M:%S')"
	git push origin main
