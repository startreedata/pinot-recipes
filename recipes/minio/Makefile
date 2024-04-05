include ../Makefile

infra: helper
	PWD=$(shell pwd) docker compose \
		-f ../pinot-compose.yml \
		-f ../minio-compose.yml \
		up -d

myminio:
	docker logs minio
	docker exec -it minio mc alias set 'myminio' 'http://minio:9000' 'miniodeepstorage' 'miniodeepstorage'
	docker exec -it minio mc admin info myminio
	docker exec -it minio mc mb myminio/deepstore
	docker exec -it minio mc ls myminio

deepstore:
	@echo "Setting managed offline flow properties in contorller"
	@curl -X POST "http://localhost:9000/cluster/configs" -H "accept: application/json" \
		-d @$(shell pwd)/config/cluster-conf.json | jq

	@curl http://localhost:9000/cluster/configs | jq


table:
	@docker exec -it pinot-controller rm -rf config
	@docker cp ./config pinot-controller:/opt/pinot/config/

	@docker exec pinot-controller ./bin/pinot-admin.sh AddTable \
		-schemaFile config/schema.json \
		-realtimeTableConfigFile config/table-realtime.json \
		-exec
	
	@TABLE=events make check_table


realtime:
	@docker run -it \
		--network recipes_default \
		--volume $(shell pwd)/config:/code/config \
		startree/helper \
		python helper.py kafka stream config/schema.json config/table-realtime.json --limit 1000


recipe: infra myminio check_pinot topic table realtime

validate:
	@test $(shell docker exec minio mc ls myminio/deepstore/events | wc -l | xargs) -gt 1 && \
		echo 'success: segments found in deepstore' || \
		echo 'no segments in deepstore' \
		exit 1


