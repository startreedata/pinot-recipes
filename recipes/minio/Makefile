include ../Makefile

AWS_ACCESS_KEY_ID=miniodeepstorage
AWS_SECRET_ACCESS_KEY=miniodeepstorage

infra: helper
	PWD=$(shell pwd) AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} docker compose \
		-f ../pinot-compose.yml \
		-f ../minio-compose.yml \
		up -d

logger:
	@docker exec pinot-controller \
		curl -X PUT -H "accept: application/json" \
		http://localhost:9000/loggers/root?level=DEBUG \
		| jq

myminio:
	@docker logs minio
	@docker exec -it minio mc alias set 'myminio' 'http://minio:9000' ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY}
	@docker exec -it minio mc admin info myminio
	@-docker exec -it minio mc mb myminio/deepstore
	@-docker exec -it minio mc mb myminio/pinot-transcript-input
	@-docker exec -it minio mc mb myminio/pinot-transcript-output
	@docker cp data/transcript.csv minio:.
	@docker exec minio mc cp transcript.csv myminio/pinot-transcript-input
	@docker exec -it minio mc ls myminio
	@docker exec -it minio mc ls myminio//pinot-transcript-input

files:
	@docker cp ./config pinot-controller:/opt/pinot/config/
	@docker cp ./data pinot-controller:/data
	-@docker exec pinot-controller mkdir /out

table: files
	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/schema.json \
		-realtimeTableConfigFile config/table.json \
		-exec
	
	@TABLE=transcript make check_table

batch:
	docker exec -it \
		pinot-controller ./bin/pinot-admin.sh LaunchDataIngestionJob   \
		-jobSpecFile ./config/job-spec.yml \
		-values ACCESS_KEY=${AWS_ACCESS_KEY_ID} SECRET_KEY=${AWS_SECRET_ACCESS_KEY}

recipe: infra myminio check_pinot logger table batch

validate:
	@test $(shell docker exec minio mc ls myminio/deepstore/events | wc -l | xargs) -gt 1 && \
		echo 'success: segments found in deepstore' || \
		echo 'no segments in deepstore' \
		exit 1


