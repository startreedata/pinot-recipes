include ../Makefile

infra: helper
	docker compose \
		-f ../pinot-compose.yml \
		up -d

table:
	@docker cp ./config pinot-controller:/opt/pinot/config/
	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/schema.json \
		-realtimeTableConfigFile config/table.json \
		-exec

	@TABLE=matches make check_table

batch:
	@docker cp ./config/job-spec.yml pinot-controller:/opt/pinot/
	@docker exec pinot-controller mkdir -p /input/
	@docker exec pinot-controller mkdir -p /data/
	@docker cp ./input/matches0.csv pinot-controller:/input/
	@docker cp ./input/matches1.csv pinot-controller:/input/

	docker exec pinot-controller \
		./bin/pinot-admin.sh LaunchDataIngestionJob \
		-jobSpecFile job-spec.yml

validate: batch
	@curl -X GET "http://localhost:9000/segments/matches?type=OFFLINE"  2>/dev/null | \
		jq -r '.[] []'

	@curl -X POST "http://localhost:9000/tasks/schedule?taskType=MergeRollupTask&tableName=matches_OFFLINE" \
  		-H "accept: application/json" 2>/dev/null | jq

recipe: infra check_pinot table

