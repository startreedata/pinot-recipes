# Apache Pinot Recipes

This repository contains Apache Pinot recipes, many referenced in StarTree developer [site](https://dev.startree.ai/).

(🍷) identifies recipes that have been recently audited and updated.


## Debezium CDC

* [Postgres](recipes/debezium-cdc/)🍷


## General Recipes

* [DateTime Strings to Timestamps](recipes/datetime-string-to-timestamp/)
* [Understanding Lookup-based Join Support](recipes/lookup-joins)🍷
* [Infer schema from JSON data](recipes/infer-schema-json-data)
* [Time boundary in hybrid tables](recipes/time-boundary-hybrid-table)🍷


## Minio / Deepstore

* [Using MinIO as Deep Store for an Offline Table](recipes/minio)🍷
* [Minio Real-Time](recipes/minio-real-time/)🍷

## Batch Data Ingestion

* [Importing JSON files](recipes/ingest-json-files)
* [Importing CSV files with columns containing spaces](recipes/csv-files-spaces-column-names/)
* [Import Data files from different directories](recipes/import-data-files-different-directories)
* [Ingest Parquet Files from a S3 Bucket into Pinot Using Spark](recipes/ingest-parquet-files-from-s3-using-spark/)

## Streaming Ingestion

* [Ingest Avro from Kafka](recipes/ingest-avro)
* [Ingest JSON files from Kafka](recipes/ingest-json-files-kafka/)🍷
* [Pulsar](recipes/pulsar/)🍷

## Upserts

* [Full Upserts](recipes/full-upserts)🍷
* [Partial Upserts](recipes/partial-upserts)

## Transformation Functions

* [Groovy Transformation Functions](recipes/groovy-transformation-functions/)
* [JSON Transformation Functions](recipes/json-transformation-functions/)
* [Chaining Transformation Functions](recipes/chaining-transformation-functions/)

## Real-Time to Offline Job (RT2OFF)

* [Manually schedule RT2OFF job](recipes/managed-offline-flow)🍷
* [Automatically schedule RT2OFF job](recipes/managed-offline-flow-automatic-scheduling)🍷
* [Backfill segment created by RT2OFF job](recipes/backfill)

## Geospatial

* [Storing Geospatial objects](recipes/geospatial)
* [Geospatial indexes](recipes/geospatial-indexing)
* [Default values for Geospatial fields](recipes/geospatial-default)

## Indexes

* [JSON indexes](recipes/json-index)
* [Update JSON index](recipes/update-json-index)
* [StarTree Index](recipes/startree-index)🍷
* [REgEx in JSON indexes](recipes/jason-regex)

## Merge and Rollup

* [Merge small segments](recipes/merge-small-segments)🍷
* [Automatically merge real-time segments](recipes/merge-small-segments-realtime)

## Querying

* [Query by segment name](recipes/query-by-segment)

## Datasets

* [Chicago Crimes](recipes/analyzing-chicago-crimes)


## Operational

* [Force Commit](recipes/force-commit)
* [Pause/Resume consumption](recipes/pause-resume)
* [Checking segment to server assignment](recipes/segment-assignment)
* [Removing server](recipes/removing-server)


## Artificial Intelligence / Similarity Search

* [Celebrity Lookalike](recipes/celebrity-lookalike/)🍷
* [GenAI](recipes/genai/)🍷
* [Vector](recipes/vector/)🍷
* [Computer Vision](recipes/video/)🍷
