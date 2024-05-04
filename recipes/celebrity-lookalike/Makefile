include ../Makefile


infra: helper
	docker compose \
		-f ../pinot-compose.yml \
		up -d

tables:
	@docker exec pinot-controller rm -rf config/
	@docker cp config/ pinot-controller:/opt/pinot/

	@docker exec pinot-controller ./bin/pinot-admin.sh \
		AddTable \
		-tableConfigFile config/table-cosine-768.json \
		-schemaFile config/schema-cosine-768.json \
		-exec

	@TABLE=celebrities_cosine_768 make check_table

loader:
# to gain access to AWS creds, we need to run this outside of docker
# pinot-admin LaunchDataIngestionJob -jobSpecFile=./config/job-spec-aws.yaml 
# pinot-admin LaunchDataIngestionJob -jobSpecFile=./config/job-spec-local-cosine.yaml 
# pinot-admin LaunchDataIngestionJob -jobSpecFile=./config/job-spec-local-l2.yaml 
	pinot-admin LaunchDataIngestionJob -jobSpecFile=./config/job-spec-local-cosine-768.yaml 

segments:

	# pinot-admin LaunchDataIngestionJob -jobSpecFile=./config/job-spec-aws-segments.yaml 


recipe: infra check_pinot tables

embeddings: clients
# to maximize threads we run this, job outside of docker
	python loader.py data/celebrities2.zip --limit 1000

app:
	flask run --port=9100


