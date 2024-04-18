include ../Makefile

URL=https://www.rtasummit.com/agenda
QUERY=big red wall and white bike

clients:
	docker build docker -t startree/vector

infra: clients helper
	docker compose \
		-f ../pinot-compose.yml \
		up -d

tables:
	@docker cp config/ pinot-controller:/opt/pinot/

	@docker exec pinot-controller ./bin/pinot-admin.sh \
		AddTable \
		-tableConfigFile config/table.json \
		-schemaFile config/schema.json \
		-exec

	@TABLE=images make check_table

recipe: infra check_pinot tables loader

loader:
	mkdir -p out
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/config \
		--volume $(shell pwd)/images:/images \
		--volume $(shell pwd)/out:/out \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		startree/vector \
		python images.py --seed

	@docker cp config/ pinot-controller:/opt/pinot/
	@docker cp out/ pinot-controller:/in

	docker exec \
		pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile ./config/jobspec.yaml

question:
	docker run -it \
		--volume $(shell pwd)/images:/images \
	 	--network recipes_default \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		startree/vector \
		python images.py --search '${QUERY}'


validate: question
	@echo 'passed'