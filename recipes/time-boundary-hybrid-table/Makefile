include ../Makefile

infra:
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		up -d

topic:
	-@docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events

table:
	@docker cp ./config/schema.json pinot-controller:/opt/pinot/
	@docker cp ./config/table-realtime.json pinot-controller:/opt/pinot/
	@docker cp ./config/table-offline.json pinot-controller:/opt/pinot/

	docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile schema.json \
		-realtimeTableConfigFile table-realtime.json \
		-offlineTableConfigFile table-offline.json \
		-exec

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table events

offline:
	@docker cp ./config/job-spec.yml pinot-controller:/opt/pinot/
	@docker exec pinot-controller mkdir -p /input/
	@docker exec pinot-controller mkdir -p /data/
	@docker cp ./input/events.json pinot-controller:/input/

	docker exec pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile job-spec.yml

realtime:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		startree/helper \
		python helper.py kafka stream config/schema.json config/table-realtime.json

data: offline realtime

recipe: infra check topic table data
	@echo "GOTO http://localhost:9000"
