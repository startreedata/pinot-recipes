include ../Makefile

clients:
	docker build docker -t startree/video

infra: clients helper
	docker compose \
		-f ../pinot-compose.yml \
		-f ../kafka-compose.yml \
		up -d

topics:
	-@docker exec kafka \
		kafka-topics.sh \
		--bootstrap-server localhost:9092 \
		--create \
		--topic video

tables:
	@docker exec pinot-controller rm -rf /opt/pinot/config/
	@docker cp ./config pinot-controller:/opt/pinot/config/

	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/people.schema.json \
		-realtimeTableConfigFile config/people.table.json \
		-exec
	@TABLE=people make check_table

	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/video.schema.json \
		-realtimeTableConfigFile config/video.table.json \
		-exec
	@TABLE=video make check_table
	

people:
	mkdir -p out
	docker run -it \
		-v $(PWD)/images:/images \
		-v $(PWD)/out:/out \
		startree/video \
		python batch.py

	@docker exec pinot-controller rm -rf /opt/pinot/config/
	@docker cp ./config pinot-controller:/opt/pinot/config/

	@docker exec pinot-controller rm -rf /in
	@docker cp ./out pinot-controller:/in

	docker exec \
		pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile config/jobspec.yaml

recipe: infra check topics tables people

app:
	streamlit run docker/application.py

video:
	# python -m venv .venv
	# source .venv/bin/activate
	pip install -r requirements.txt
	python video.py
