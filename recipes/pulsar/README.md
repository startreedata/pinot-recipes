# Pulsar

> In this recipe we'll learn how to ingest data from Apache Pulsar.

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
cd pinot-recipes/recipes/pulsar
```

Build Pulsar plugin:

```bash
git clone git@github.com:apache/pinot.git
cd pinot
git checkout release-0.10.0
```

```bash
cd pinot-plugins/pinot-stream-ingestion/pinot-pulsar
mvn clean install -DskipTests
```

The Pulsar plugin is in `target/pinot-pulsar-0.10.0-shaded.jar` and we'll copy that into the `plugins` directory.

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-pulsar bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```

Import message into Kafka:

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done | docker exec -i kafka-pulsar /opt/kafka/bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic events
```

Query Pinot:

```sql
select * 
from events
```
