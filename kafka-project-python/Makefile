# Set shell
SHELL=/bin/bash -e -o pipefail

### Dependencies and githook setup ###
.PHONY: deps pre-commit lint

deps: 
	pip install -r requirements.txt

pre-commit:
	pre-commit install -t pre-commit -t commit-msg


### Development ###
lint:
	pre-commit run --all-files

### Start cluster ###
zookeeper-start:
	cd ~/kafka_2.13-2.8.0; zookeeper-server-start config/zookeeper.properties

kafka-start:
	cd ~/kafka_2.13-2.8.0; kafka-server-start config/server.properties

faust-start:
	python -m faust -A kafka_streams_filter_tweets worker -l info
