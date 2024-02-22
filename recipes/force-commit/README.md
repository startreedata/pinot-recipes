# Force Commit

> In this recipe we'll learn how to force commit segments.

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
cd pinot-recipes/recipes/force-commit
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network forcecommit \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-forcecommit" \
    -exec
```

Import messages into Kafka:

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

Query Pinot:

```sql
select $segmentName, ToDateTime(max(ts), 'YYYY-MM-dd HH:mm:ss') as maxTs, count(*)
from events
group by $segmentName
order by maxTs desc
limit 100
```

Update the segment threshold from 500k to 100k:

```bash
docker run \
   --network forcecommit \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-newthreshold.json \
     -controllerHost "pinot-controller-forcecommit" \
    -exec -update
```

Force commit to have it applied now.

```bash
curl -X POST "http://localhost:9000/tables/events/forceCommit" -H "accept: application/json"
```