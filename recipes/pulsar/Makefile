include ../Makefile

infra: helper
	docker compose \
		-f ../pulsar-compose.yml \
		-f ../pinot-compose.yml \
		up -d

table:
	@docker cp ./config/schema.json pinot-controller:/opt/pinot/
	@docker cp ./config/table.json pinot-controller:/opt/pinot/

	docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile schema.json \
		-realtimeTableConfigFile table.json \
		-exec

	@TABLE=events make check_table

realtime:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		startree/helper \
		python helper.py pulsar stream config/schema.json config/table.json


recipe: infra check_pinot table realtime

validate: helper
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check results 'select count(*) from events' 1000
	@echo 'results are valid'

