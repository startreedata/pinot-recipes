

infra:
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		-f ../datagen-compose.yml \
		up -d
	
	@echo 'waiting for pinot'
	bash -c 'while [[ "$(shell curl --insecure -s -o /dev/null -w %{http_code} http://localhost:9000)" != "200" ]]; do echo ''.'' && sleep 5; done'
	@echo 'waiting for kafka'
	bash -c 'while [[ "$(shell curl --insecure -s -o /dev/null -w %{http_code} http://localhost:9092)" != "000" ]]; do echo '','' && sleep 5; done'
        
topic:
	docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events

table:
	docker cp ./config/schema.json pinot-controller:/opt/pinot/
	docker cp ./config/table-realtime.json pinot-controller:/opt/pinot/
	docker cp ./config/table-offline.json pinot-controller:/opt/pinot/

	docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile schema.json \
		-realtimeTableConfigFile table-realtime.json \
		-offlineTableConfigFile table-offline.json \
		-exec

	sleep 5

offline:
	docker cp ./config/job-spec.yml pinot-controller:/opt/pinot/
	docker exec pinot-controller mkdir -p /input/
	docker exec pinot-controller mkdir -p /data/
	docker cp ./input/events.json pinot-controller:/input/

	docker exec pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile job-spec.yml

realtime:
	docker run -it \
		--network recipes_default \
		--volume ${PWD}/config:/code/config \
		recipes-producer \
		python producer.py config/schema.json config/table-realtime.json

data: offline realtime

recipe: infra topic table data

clean:
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		-f ../datagen-compose.yml \
		down
