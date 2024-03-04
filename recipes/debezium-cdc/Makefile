
infra:
	docker compose \
		-f ../pinot-compose.yml \
		-f ../kafka-compose.yml \
		-f ../postgres-compose.yml \
		-f docker-compose.yml up -d

kafka:
	-docker exec -it kafka \
		kafka-topics.sh \
		--bootstrap-server kafka:9092 \
		--create \
		--topic debezium_REALTIME

postgres:
	curl -O https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
	unzip dvdrental.zip
	docker cp sql/init.sql postgres:.
	docker cp sql/cdc.sql postgres:.
	docker cp dvdrental.tar postgres:.
	docker exec -it postgres psql -h localhost -U postgres -f init.sql
	sleep 5
	docker exec -it postgres pg_restore -h localhost -U postgres -d dvdrental dvdrental.tar
	sleep 5
	docker exec -it postgres psql -h localhost -U postgres -d dvdrental -f cdc.sql
	sleep 5

connect:
	-curl -X DELETE http://localhost:8083/connectors/dvdrental-connector | jq
	curl http://localhost:8083/connectors | jq
	
	curl -X POST http://localhost:8083/connectors \
		-H 'Content-Type: application/json' \
   		-d @debezium/register-postgres.json | jq

	docker exec -it kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

tables:
	docker cp config/rental.json pinot-controller:/opt/pinot/
	docker cp config/rental.table.config.json pinot-controller:/opt/pinot/

	docker exec -it pinot-controller ./bin/pinot-admin.sh DeleteSchema \
		-schemaName rental
		-exec
	
	docker exec -it pinot-controller ./bin/pinot-admin.sh DeleteTable \
		-tableName rental
		-exec
	
	sleep 5

	docker exec -it pinot-controller ./bin/pinot-admin.sh AddTable \
		-tableConfigFile rental.table.config.json \
		-schemaFile rental.json \
		-exec

recipe: infra kafka postgres connect tables

clean:
	-rm dvdrental*
	-docker compose \
		-f ../pinot-compose.yml \
		-f ../kafka-compose.yml \
		-f ../postgres-compose.yml \
		-f docker-compose.yml down
