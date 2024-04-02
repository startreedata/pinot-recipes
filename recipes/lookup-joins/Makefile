include ../Makefile

infra:
	docker build ../docker/helper/ -t startree/helper
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		up -d

topic:
	-@docker exec kafka \
		kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic orders

table:
	@docker cp ./config/customers_schema.json pinot-controller:/opt/pinot/
	@docker cp ./config/orders_schema.json pinot-controller:/opt/pinot/
	@docker cp ./config/customers_table.json pinot-controller:/opt/pinot/
	@docker cp ./config/orders_table.json pinot-controller:/opt/pinot/

	-docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile customers_schema.json \
		-realtimeTableConfigFile customers_table.json \
		-exec

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table customers

	-docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile orders_schema.json \
		-offlineTableConfigFile orders_table.json \
		-exec

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table orders

offline:
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table orders

	@docker cp ./config/customers_job-spec.yml pinot-controller:/opt/pinot/
	@docker exec pinot-controller mkdir -p /data/
	@docker cp ./data/customers.csv pinot-controller:/data/

	docker exec pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile customers_job-spec.yml

realtime:
	@docker run -it \
		--network recipes_default \
		-v $(shell pwd)/config/:/code/config/ \
		startree/helper \
		python helper.py \
			kafka stream  \
			config/orders_schema.json \
			config/orders_table.json

recipe: infra check topic table realtime offline

clean:
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		down
