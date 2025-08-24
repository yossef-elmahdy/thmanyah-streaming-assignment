# Run everything in sequence
all: setup up wait register-connector health run-faust mock-data logs

# Python Setup
setup:
	bash scripts/setup.sh

# Docker Compose Up
up:
	docker compose up -d

# Wait for all services to be ready (1 minute)
wait:
	@echo "Waiting 1 minute for services to start..."
	sleep 60

# Register Debezium Connector
register-connector:
	source .venv/bin/activate && \
	python scripts/register_debezium_connector.py

health:
	curl -s http://localhost:8083/connectors || echo "Kafka Connect not ready yet"

# Run Faust App
run-faust:
	bash scripts/clean_and_run_faust.sh

# Run Mock Data Generator
mock-data:
	bash scripts/run_mock_data.sh

# View Docker logs
logs:
	docker compose logs -f

# Stop all containers (Optional)
down:
	docker compose down


# Clean all containers, volumes (Optional)
clean:
	docker compose down -v

# Backfill script (Optional)
backfill:
	source .venv/bin/activate && \
	python scripts/backfill.py

