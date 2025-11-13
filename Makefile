TOPIC ?=

.PHONY: run build up

build:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	docker compose build app

run:
ifndef TOPIC
	$(error TOPIC is required. Usage: make run TOPIC="AI in Healthcare")
endif
	docker compose run --rm \
		-e WATCH_MODE=false \
		app \
		--topic "$(TOPIC)"

up:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	docker compose up app -d

