# Full Upserts

> In this recipe we'll learn how to use upsert functionality.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.12.0</td>
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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-full

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/full-upserts
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker run \
   --network fullupserts \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/orders_schema.json \
     -tableConfigFile /config/orders_table.json \
     -controllerHost "pinot-controller" \
    -exec

```

Open a tab to import messages into Kafka:

```bash
echo -e '
{"order_id":1,"customer_id":104,"order_status":"IN_TRANSIT","amount":29.35,"ts":"1632467063"}
{"order_id":2,"customer_id":105,"order_status":"COMPLETED","amount":3.24,"ts":"1618931459"}
{"order_id":3,"customer_id":103,"order_status":"OPEN","amount":9.77,"ts":"1626484196"}
{"order_id":4,"customer_id":104,"order_status":"COMPLETED","amount":90.35,"ts":"1623066325"}
{"order_id":5,"customer_id":105,"order_status":"OPEN","amount":55.52,"ts":"1635543905"}
' | kcat -P -b localhost:9092 -t orders
```

Paste the following:

```json
{"order_id":1,"customer_id":104,"order_status":"IN_TRANSIT","amount":29.35,"ts":"1632467063"}
{"order_id":2,"customer_id":105,"order_status":"COMPLETED","amount":3.24,"ts":"1618931459"}
{"order_id":3,"customer_id":103,"order_status":"OPEN","amount":9.77,"ts":"1626484196"}
{"order_id":4,"customer_id":104,"order_status":"COMPLETED","amount":90.35,"ts":"1623066325"}
{"order_id":5,"customer_id":105,"order_status":"OPEN","amount":55.52,"ts":"1635543905"}
```

Query Pinot:

```sql
select * 
from orders 
limit 10
```

Go back to the Kafka tab and paste the following:

```json
echo -e '
{"order_id":5,"customer_id":105,"order_status":"CANCELLED","amount":55.52,"ts":"1635543948"}
' | kcat -P -b localhost:9092 -t orders
```
