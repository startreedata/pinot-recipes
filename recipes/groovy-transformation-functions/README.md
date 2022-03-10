# Groovy Transformation Functions

> In this recipe we'll learn how to use Groovy transformation functions to ingest events from Kafka.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.3</td>
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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/groovy-transformation-functions

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/groovy-transformation-functions
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `events` table:

```bash
docker exec -it pinot-controller-groovy bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

Add events into Kafka:

```bash
printf '{"timestamp": "2019-10-09 21:25:25", "payload": {"firstName": "James", "lastName": "Smith", "before": {"id": 2}, "after": { "id": 3}}}
{"timestamp": "2019-10-10 21:33:25", "payload": {"firstName": "John", "lastName": "Gates", "before": {"id": 2}}}\n' |
docker exec -i kafka-groovy /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic events
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from events 
limit 10
```
