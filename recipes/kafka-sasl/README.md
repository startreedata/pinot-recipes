# Kafka SASL

> In this recipe we'll learn how to configure Pinot to work with Kafka with SASL enabled.

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/kafka-sasl

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/kafka-sasl
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Import message into Kafka:

```bash
python datagen.py |
kcat -P -b localhost:9092 -F kafka-config/kafka_client_kcat.conf -t events
```

Consume messages from Kafka:

```bash
kcat -C -b localhost:9092 -F kafka-config/kafka_client_kcat.conf -t events
``` 

Add table and schema:

```bash
docker run \
   --network sasl \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0  AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -controllerHost "pinot-controller-sasl" \
  -exec
```

Query Pinot:

```sql
select * 
from events
```
