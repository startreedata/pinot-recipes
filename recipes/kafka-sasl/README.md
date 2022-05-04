# Kafka SASL

> In this recipe we'll learn how to configure Pinot to work with Kafka with SASL enabled.

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/kafka-sasl

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/kafka-sasl
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Import message into Kafka:

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done | docker exec -i kafka-sasl /opt/kafka/bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic events \
    --producer.config /etc/kafka/kafka_client.conf
```

Consume messages from Kafka:

```bash
docker exec -i kafka-sasl /opt/kafka/bin/kafka-console-consumer.sh \
   --bootstrap-server localhost:9093  \
   --consumer.config /etc/kafka/kafka_client.conf \
   --topic events \
   --from-beginning
``` 

Add table and schema:

```bash
docker exec -it pinot-controller-sasl bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```

Query Pinot:

```sql
select * 
from events
```
