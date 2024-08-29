include ../Makefile

infra: 
	@docker-compose up

batch:
	@docker exec -it pinot-controller cp /data/* /opt/pinot/data
	@docker exec -it pinot-controller \
	./bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /config/jobspec.yaml 

recipe: infra check_pinot logger batch

validate:

clean:
	@docker-compose down