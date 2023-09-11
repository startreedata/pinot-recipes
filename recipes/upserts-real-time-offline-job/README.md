# Full Upserts and the real-time to offline job

> In this recipe we'll learn how to use upsert functionality with the real-time to offline job.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.3</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/orders_schema.json</a></td>
  </tr>
    <tr>
    <td>Table Config</td>
    <td><a href="config/table.json">config/orders_table.json</a></td>
  </tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-full -->

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/upserts-real-time-offline-job
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add offline table and schema:

```bash
docker run \
   --network upserts \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/orders_schema.json \
     -tableConfigFile /config/orders_offline_table.json \
     -controllerHost "pinot-controller" \
    -exec
```

Add real-time table:

```bash
wget -q --method=POST "http://localhost:9000/tables?validationTypesToSkip=ALL" \
     --header="accept: application/json" \
     --header="Content-Type: application/json" \
     --body-file=config/orders_table.json \
     -O -
```


Import messages into Kafka:

```bash
echo -e '
{"order_id":1,"customer_id":104,"order_status":"OPEN","amount":29.35,"ts":"1632463351000"}
{"order_id":1,"customer_id":104,"order_status":"IN_TRANSIT","amount":29.35,"ts":"1632463361000"}
{"order_id":1,"customer_id":104,"order_status":"COMPLETED","amount":29.35,"ts":"1632463391000"}
{"order_id":2,"customer_id":105,"order_status":"COMPLETED","amount":3.24,"ts":"1632467065000"}
{"order_id":3,"customer_id":103,"order_status":"OPEN","amount":9.77,"ts":"1632467066000"}
{"order_id":4,"customer_id":104,"order_status":"OPEN","amount":55.52,"ts":"1632467068000"}
{"order_id":4,"customer_id":104,"order_status":"CANCELLED","amount":55.52,"ts":"1632467070000"}
{"order_id":5,"customer_id":105,"order_status":"OPEN","amount":12.22,"ts":"1632667070000"}
{"order_id":5,"customer_id":105,"order_status":"IN_TRANSIT","amount":12.22,"ts":"1632667170000"}
{"order_id":5,"customer_id":105,"order_status":"COMPLETED","amount":12.22,"ts":"1632677270000"}
{"order_id":6,"customer_id":106,"order_status":"OPEN","amount":13.94,"ts":"1632677270400"}
{"order_id":7,"customer_id":107,"order_status":"OPEN","amount":20.32,"ts":"1632677270403"}
{"order_id":8,"customer_id":108,"order_status":"OPEN","amount":45.11,"ts":"1632677270508"}
{"order_id":9,"customer_id":109,"order_status":"OPEN","amount":129.22,"ts":"1632677270699"}
' | kcat -P -b localhost:9092 -t orders
```

Query Pinot:

```sql
select * 
from orders 
where order_id = 1
```

Run the Real-Time to Offline Job:

```bash
tableName="orders_REALTIME"
wget -q --method=POST \
  "http://localhost:9000/tasks/schedule?taskType=RealtimeToOfflineSegmentsTask&tableName=${tableName}" \
  --header="accept: application/json" -O -
```

Now, query for `order_id=1`:

```sql
select * 
from orders 
where order_id = 1
limit 10
```

Backfill the offline segment with the records in [data/orders.json](data/orders.json)

```bash
docker run \
   --network upserts \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml \
  -values segmentName='orders_1632463351000_1632467070000_0'
```

Query for `order_id=1` again:

```sql
select * 
from orders 
where order_id = 1
limit 10
```


