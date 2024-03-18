include ../Makefile

infra: helper
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		up -d

up: helper infra check

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

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table webtraffic

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table webtraffic_inverted

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table webtraffic_stree


realtime:
	@docker run -it \
		--network recipes_default \
		--volume ${PWD}/config:/code/config \
		startree/helper \
		python helper.py kafka stream config/base/schema.json config/base/table.json

recipe: up tables realtime
