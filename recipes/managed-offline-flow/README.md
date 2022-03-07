# Real-Time to Offline 

> In this recipe we'll learn how to use Pinot offline managed flow.

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
cd pinot-recipes/recipes/real-time-to-offline
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-rt bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table-realtime.json   \
  -schemaFile /config/schema.json -exec
```

```bash
docker exec -it pinot-controller-rt bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table-offline.json   \
  -schemaFile /config/schema.json -exec
```

Import message into Kafka:

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done |
docker exec -i kafka-rt /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic events
```

Query Pinot:

```sql
select * 
from events
```