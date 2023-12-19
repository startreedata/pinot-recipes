# Ingesting Avro messages

> In this recipe we'll learn how to ingest JSON files.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
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

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/ingest-json-files -->

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/ingest-avro
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Ingest data into Kafka

```bash
pip install avro confluent-kafka click faker requests
```

```bash
python datagen.py| python kafkaproducer.py
```

Check data is ingesting:

```bash
kcat -C -b localhost:9092 -t person-topic -r localhost:8081 -s value=avro
```

Add tables and schema:

```bash
docker run \
   --network ingestavro \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller" \
    -exec
```

Query via the Pinot UI:

```sql
select * 
from people 
where person.friend_ids <> 'null'
AND person.interests <> 'null'
and ARRAYLENGTH(person.interests) > 1

limit 10
```