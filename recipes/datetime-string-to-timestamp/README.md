# Converting DateTime strings to Timestamps

> In this recipe we'll learn how to import DateTime strings into Pinot.

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/datetime-string-to-timestamp

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/datetime-string-to-timestamp
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-datetime bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```

Import message into Kafka:

```bash
printf '{"timestamp1": "2019-10-09 22:25:25", "timestamp2": "1570656325000", "timestamp3": "10/09/2019 22:25:25"}\n' |
docker exec -i kafka-datetime /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic dates
```

Query Pinot:

```sql
select * 
from dates
```
