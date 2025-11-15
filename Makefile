# Запуск fastapi
run-fastapi:
	uvicorn app.main:app --reload

# Запуск и сборка контейнеров
build-docker:
	docker-compose up --build

# Запуск контейнеров
start-docker:
	docker-compose up

# Остановка контейнеров
stop-docker:
	docker-compose down

# Полная очистка
clean-docker:
	docker-compose down -v --remove-orphans
	docker rmi spravochnik-web || true

# Полная пересборка с чистой БД
rebuild-docker:
	docker-compose down -v --remove-orphans
	docker-compose up --build
