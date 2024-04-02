include ../Makefile

infra: helper
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		up -d

up: helper infra check

topic:
	-@docker exec kafka \
		kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic webtraffic

tables:
	@docker cp ./config pinot-controller:/opt/pinot/config/

	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/base/schema.json \
		-realtimeTableConfigFile config/base/table.json \
		-exec
	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/inverted/schema.json \
		-realtimeTableConfigFile config/inverted/table.json \
		-exec

	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/startree/schema.json \
		-realtimeTableConfigFile config/startree/table.json \
		-exec

	@TABLE=webtraffic make check_table
	@TABLE=webtraffic_inverted make check_table
	@TABLE=webtraffic_stree make check_table


realtime:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		startree/helper \
		python helper.py kafka stream config/base/schema.json config/base/table.json

recipe: up topic tables realtime
