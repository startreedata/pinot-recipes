# Backfill

> In this recipe, we'll learn how to replace a segment moved from a real-time to offline table.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/orders_schema.json</a></td>
  </tr>
    <tr>
    <td>Real-Time Table Config</td>
    <td><a href="config/orders_table.json">config/orders_table.json</a></td>
  </tr>
  <tr>
  <td>Offline Table Config</td>
  <td><a href="config/orders_offline_table.json">config/orders_offline_table.json</a></td>
</tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-full -->

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/backfill
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network backfill \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/orders_schema.json \
     -tableConfigFile /config/orders_table.json \
     -controllerHost "pinot-controller" \
    -exec
```

```bash
docker run \
   --network backfill \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/orders_schema.json \
     -tableConfigFile /config/orders_offline_table.json \
     -controllerHost "pinot-controller" \
    -update -exec
```

Import messages into Kafka:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server kafka:9092 --topic orders

{"order_id":1,"customer_id":101,"order_status":"OPEN","amount":13.29,"ts":"1632463351000"}
{"order_id":2,"customer_id":102,"order_status":"IN_TRANSIT","amount":209.35,"ts":"1632463361000"}
{"order_id":3,"customer_id":103,"order_status":"COMPLETED","amount":199.35,"ts":"1632463391000"}
{"order_id":4,"customer_id":105,"order_status":"COMPLETED","amount":3.24,"ts":"1632467065000"}
{"order_id":5,"customer_id":103,"order_status":"OPEN","amount":9.77,"ts":"1632467066000"}
{"order_id":6,"customer_id":104,"order_status":"OPEN","amount":55.52,"ts":"1632467068000"}
{"order_id":7,"customer_id":104,"order_status":"CANCELLED","amount":52.54,"ts":"1632467070000"}
{"order_id":8,"customer_id":105,"order_status":"OPEN","amount":13.29,"ts":"1632667070000"}
{"order_id":9,"customer_id":105,"order_status":"IN_TRANSIT","amount":2.92,"ts":"1632667170000"}
{"order_id":10,"customer_id":105,"order_status":"COMPLETED","amount":12.22,"ts":"1632677270000"}
{"order_id":11,"customer_id":106,"order_status":"OPEN","amount":13.94,"ts":"1632677270400"}
{"order_id":12,"customer_id":107,"order_status":"OPEN","amount":20.32,"ts":"1632677270403"}
{"order_id":13,"customer_id":108,"order_status":"OPEN","amount":45.11,"ts":"1632677270508"}
{"order_id":14,"customer_id":109,"order_status":"OPEN","amount":129.22,"ts":"1632677270699"}
```

Run the Real-Time to Offline Job:

```bash
tableName="orders_REALTIME"
curl -X POST "http://localhost:9000/tasks/schedule?taskType=RealtimeToOfflineSegmentsTask&tableName=${tableName}" \
  -H "accept: application/json" 2>/dev/null | jq '.'
```

Update the time boundary so that it starts from the latest time in the offline table:

```bash
curl -X POST \
  "http://localhost:9000/tables/orders/timeBoundary" \
  -H "accept: application/json"
```

Backfill the first 7 records to increase the amount by 20%:

```bash
docker run \
   --network backfill \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
    -jobSpecFile /config/job-spec.yml \
    -values segmentName='orders_1632463351000_1632467070000_0' \
    -values pinotController=http://pinot-controller:9000
```

Query the `orders` table:

```sql
select order_id, customer_id, order_status, amount,
       ToDateTime(ts, 'YYYY-MM-dd HH:mm:ss') AS tsString,
       ToDateTime(1632463470000, 'YYYY-MM-dd HH:mm:ss') AS boundary
from orders
ORDER BY order_id
limit 10
```
