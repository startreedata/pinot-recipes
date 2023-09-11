# Converting DateTime strings to Timestamps

> In this recipe we'll learn how to import DateTime strings into Pinot.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.12.0</td>
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
docker run \
   --network datetime \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -controllerHost "pinot-controller-datetime" \
  -exec
```

Import message into Kafka:

```bash
printf '{"timestamp1": "2019-10-09 22:25:25", "timestamp2": "1570656325000", "timestamp3": "10/09/2019T22:25:25"}\n' |
kcat -P -b localhost:9092 -t dates
```

Query Pinot:

```sql
select * 
from dates
```
