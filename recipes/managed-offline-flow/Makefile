include ../Makefile

infra: helper
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		up -d

topic:
	-@docker exec kafka \
		kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic events

tables:
	@docker cp ./config pinot-controller:/opt/pinot/config/

	@docker exec -it pinot-controller bin/pinot-admin.sh AddTable \
		-tableConfigFile config/table-offline.json \
		-offlineTableConfigFile  config/table-offline.json \
		-realtimeTableConfigFile config/table-realtime.json \
		-schemaFile config/schema.json \
		-exec

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table events

realtime:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		startree/helper \
		python helper.py kafka stream config/schema.json config/table-realtime.json \
		--limit 20000

manage_offline_flow:

	@echo "Setting managed offline flow properties in contorller"
	curl -X POST "http://localhost:9000/cluster/configs" -H "accept: application/json" \
		--data '{"RealtimeToOfflineSegmentsTask.timeoutMs": "600000", "RealtimeToOfflineSegmentsTask.numConcurrentTasksPerInstance": "1" }' | jq
	
	@echo "Scheduling the task"
	curl -X POST "http://localhost:9000/tasks/schedule?taskType=RealtimeToOfflineSegmentsTask&tableName=events_REALTIME" \
  		-H "accept: application/json" | jq

	@echo "Capture the related log."
	docker exec -it pinot-controller grep -rni --color "\[RealtimeToOff" logs/pinot-all.log

	curl -X POST \
		"http://localhost:9000/tables/events/timeBoundary" \
		-H "accept: application/json" | jq

recipe: infra check topic tables realtime
	@echo "GOTO http://localhost:9000"

