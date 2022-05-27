# Working with nested JSON documents

> In this recipe we'll learn how to work with nested JSON documents.

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

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/json-nested
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Create Kafka topic:

```bash
docker exec -i kafka-json kafka-topics.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events \
  --partitions 5 \
  --create
```

Generate schema:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -timeColumnName first_air_date \
  -metrics "number_of_episodes,popularity"\
  -pinotSchemaName=tv_shows \
  -jsonFile=/data/shows.json \
  -outputDir=/config
```

Open another tab to add the `movies` table:


```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -schemaFile /config/tv_shows.json \
  -tableConfigFile /config/table.json   \
  -exec
```

Import [data/movies.json](data/movies.json) into Pinot:

```bash
docker exec -i kafka-json kafka-console-producer.sh \
  --bootstrap-server kafka-json:9092 \
  --topic events < data/shows.json
```

Navigate to http://localhost:9000/#/query and run the following queries:

```sql
select * 
from users_no_flatten 
limit 10
```

```sql
select * 
from users_flatten 
limit 10
```
