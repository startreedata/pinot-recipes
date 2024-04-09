
helper:
	docker build ../docker/helper/ -t startree/helper

check_kafka:
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py kafka check broker

check_pinot:
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check controller

check: check_pinot check_kafka

check_table:
	@# USAGE:
	@# TABLE=my_table make check_table
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check table ${TABLE}

clean:
	@docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		-f ../postgres-compose.yml \
		-f ../pulsar-compose.yml \
		-f ../minio-compose.yml \
		-f ../flink-compose.yml \
		down

validate:
	@echo "VALIDATION HAS NOT BEEN IMPLEMENTED"

test: recipe validate clean

test_all:
	make test -C debezium-cdc/
	make test -C full-upserts/
	make test -C ingest-json-files-kafka/
	make test -C lookup-joins/
	make test -C startree-index/
	make test -C time-boundary-hybrid-table/
	make test -C managed-offline-flow/
	make test -C merge-small-segments/
	make test -C pulsar/
	make test -C minio-real-time/

