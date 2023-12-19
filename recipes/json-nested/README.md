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
docker compose up
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
docker run \
   --network json \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 JsonToPinotSchema \
  -timeColumnName first_air_date \
  -metrics "number_of_episodes,popularity"\
  -pinotSchemaName=tv_shows \
  -jsonFile=/data/shows.json \
  -outputDir=/config
```


```bash
sudo chown `whoami`:`whoami` config/tv_shows.json
```

Open another tab to add the `movies` table:


```bash
docker run \
   --network json \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0  AddTable   \
  -schemaFile /config/tv_shows.json \
  -tableConfigFile /config/table.json   \
  -controllerHost "pinot-controller-json" \
  -exec
```

Import [data/shows.json](data/shows.json) into Pinot:

```bash
cat data/shows.json |
kcat -P -b localhost:9092 -t events
```

Navigate to http://localhost:9000/#/query and run the following queries:

```sql
select * 
from tv_shows
limit 10
```
