include ../Makefile

infra: helper
	docker compose \
		-f ../pinot-compose.yml \
		-f ../kafka-compose.yml \
		-f ../flink-compose.yml \
		-f docker-compose.yml \
		up -d

topics:
	-docker exec kafka kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic documentation

	-docker exec kafka kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic doc_embeddings

tables:
	docker cp config/ pinot-controller:/opt/pinot/

	docker exec pinot-controller ./bin/pinot-admin.sh \
		AddTable \
		-tableConfigFile config/table.json \
		-schemaFile config/schema.json \
		-exec

	@TABLE=documentation make check_table

recipe: build infra topic tables

loader:
	@docker run -it \
	 	--network rag_default \
		genai \
		python loader.py $(URL)

question:
	@docker run -it \
	 	--network rag_default \
		genai \
		python genai.py



recipe: infra check kafka postgres connect tables

