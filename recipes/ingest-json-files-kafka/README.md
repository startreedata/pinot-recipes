# Ingesting JSON files

> In this recipe we'll learn how to ingest JSON files.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/schema.json</a></td>
  </tr>
    <tr>
    <td>Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
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
docker compose -f ../pinot-compose.yml -f ../kafka-compose.yml up -d
```

Open another tab to add the `movies` table:

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
docker cp config/schema.json pinot-controller:/opt/pinot
docker cp config/table.json pinot-controller:/opt/pinot
docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile table.json   \
  -schemaFile schema.json \
  -exec
```

Import [data/ingest1.jsonl](data/import1.jsonl) and [data/ingest2.jsonl](data/import2.jsonl) into Pinot:

```bash
cat data/import1.jsonl | docker exec -i kafka kafka-console-producer.sh \
  --bootstrap-server kafka:9092 \
  --topic events
```

```bash
cat data/import2.jsonl | docker exec -i kafka kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic events
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movies 
limit 10
```
