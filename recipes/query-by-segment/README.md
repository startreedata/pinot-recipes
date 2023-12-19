# Query by segment

> In this recipe we'll learn how to query a table by segment name.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/schema.json</a></td>
  </tr>
    <tr>
    <td>Real-Time Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-full -->

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/query-by-segment
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network querysegment \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-querysegment" \
    -exec
```

Remove the `-arm64` suffix from the Apache Pinot image name if you aren't using the Mac M1/M2.

Import messages into Kafka:

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

Query Pinot:

```sql
select $segmentName, count(*)
from events
group by $segmentName
limit 10
```


```sql
select *
from events
-- Change the segment name to match one that's returned by the previous query
WHERE $segmentName = 'events__0__14__20230330T1003Z'
limit 10
```
