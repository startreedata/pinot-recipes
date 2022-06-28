# Ingesting JSON files

> In this recipe we'll learn how to ingest JSON files.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.10.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/schema.json</a></td>
  </tr>
    <tr>
    <td>Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
      <tr>
    <td>Ingestion Job</td>
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/ingest-json-files

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/ingest-json-files-kafka
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `movies` table:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

Create Kafka topic:

```bash
docker exec -i kafka-json kafka-topics.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events \
  --partitions 5 \
  --create
```

Import [data/ingest1.jsonl](data/import1.jsonl) and [data/ingest2.jsonl](data/import2.jsonl) into Pinot:

```bash
docker exec -i kafka-json kafka-console-producer.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events < data/import1.jsonl
```

```bash
docker exec -i kafka-json kafka-console-producer.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events < data/import2.jsonl
```

Check the message in the Kafka topic:

```bash
docker exec -i kafka-json kafka-console-consumer.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events \
  --from-beginning
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movies 
limit 10
```
