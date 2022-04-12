# Kafka SASL

> In this recipe we'll learn how to configure Pinot to work with Kafka with SSL and SASL enabled.

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
</table>



***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/kafka-ssl-sasl
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Create a Kafka Cluster on [Confluent Cloud](https://confluent.cloud/), add an `events` topic, and publish the following messages via the UI:

```json
{"ts": "1649757242937", "uuid": "fc43b2fafbf64d9e8dff8d6be75d881d", "count": 308}
{"ts": "1649757242941", "uuid": "11f2500386ec42be84debba1d5bfd2f7", "count": 515}
{"ts": "1649757242945", "uuid": "f2dcf496957146eaa12605c5d8c005a0", "count": 142}
```

Update the following properties in [config/table.json](config/table.json):


```yaml
"stream.kafka.broker.list": "<bootstrap.servers>",
"sasl.jaas.config":"org.apache.kafka.common.security.scram.ScramLoginModule required username=\"<cluster-api-key>\" password=\"<cluster-api-secret>\";",
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
