# Configuring segment threshold

> In this recipe we'll learn how to configure the segment threshold for real-time tables

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

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/configuring-segment-threshold
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-segment bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```

Import message into Kafka:

```bash
printf '{"timestamp1": "2019-10-09 22:25:25", "timestamp2": "1570656325000", "timestamp3": "10/09/2019 22:25:25"}\n' |
docker exec -i kafka-segment /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic dates
```

Query Pinot:

```sql
select * 
from dates
```
