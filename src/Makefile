# Makefile for Traffic Processor – standalone deployment

.PHONY: help build attach attach-cnss clean

help:
	@echo "Available targets:"
	@echo "  build          – build the traffic-processor Docker image"
	@echo "  attach APP     – attach traffic-processor to a running container APP"
	@echo "  attach-cnss    – attach traffic-processor to the cnss stack (uses docker-compose)"
	@echo "  clean          – remove the traffic-processor image"

# Build the standalone image
build:
	docker build -t traffic-processor:latest -f Traffic_Processor/Dockerfile Traffic_Processor

# Attach to any running container (pass APP=container_name)
attach:
	@if [ -z "$(APP)" ]; then \
		echo "Usage: make attach APP=container_name"; \
		exit 1; \
	fi
	docker run --rm \
		--network container:$(APP) \
		-e CNSS_URL=http://cnss:38080/load \
		-e INTERFACE=eth0 \
		--name tp-$(APP) \
		traffic-processor:latest

# Attach to the cnss stack (requires cnss+postgres to be up via docker-compose)
attach-cnss:
	docker run --rm \
		--network src_swp-net \
		-e CNSS_URL=http://cnss:38080/load \
		-e INTERFACE=eth0 \
		--name tp-cnss \
		traffic-processor:latest

# Remove the built image
clean:
	docker rmi traffic-processor:latest || true