include ../Makefile

recipe:
	docker compose -f ../kafka-compose.yml -f ../pinot-compose.yml up -d

down:
	docker compose -f ../kafka-compose.yml -f ../pinot-compose.yml down
