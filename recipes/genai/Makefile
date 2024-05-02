include ../Makefile

URL=https://www.rtasummit.com/agenda
QUERY='when and where does kishore speak in rtasummit'

clients:
	docker build docker -t startree/genai

infra: clients helper
	docker compose \
		-f ../pinot-compose.yml \
		-f ../kafka-compose.yml \
		up -d

topics:
	-@docker exec kafka kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic documentation

tables:
	@docker cp config/ pinot-controller:/opt/pinot/

	@docker exec pinot-controller ./bin/pinot-admin.sh \
		AddTable \
		-tableConfigFile config/table.json \
		-schemaFile config/schema.json \
		-exec

	@TABLE=documentation make check_table

recipe: infra check topics tables

loader:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		startree/genai \
		python loader.py ${URL}

question: clients
	@docker run -it \
	 	--network recipes_default \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		startree/genai \
		python genai.py ${QUERY}


validate: loader question
	@echo 'passed'