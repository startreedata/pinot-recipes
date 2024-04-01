include ../Makefile

infra:
	docker compose -f ../pinot-compose.yml -f ../kafka-compose.yml up -d

recipe: infra check
	

