
helper:
	docker build ../docker/helper/ -t startree/helper

check:
	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py pinot check controller

	@docker run -it \
		--network recipes_default \
		startree/helper \
		python helper.py kafka check broker

clean:
	docker compose \
		-f ../kafka-compose.yml \
		-f ../pinot-compose.yml \
		-f ../postgres-compose.yml \
		down
