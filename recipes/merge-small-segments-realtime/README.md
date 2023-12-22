# Merge segments in real-time table

> In this recipe we'll learn how to automatically merge segments in real-time tables.

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
    <td>Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/merge-small-segments -->

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/merge-small-segments-realtime
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network mergesegments \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-mergesegments" \
    -exec
```

Import messages into Kafka:

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

Run the following query to get a list of segment and the number of records that each holds:

```sql
select $segmentName, count(*), 
       ToDateTime(min(ts), 'YYYY-MM-dd HH:mm:ss') AS minDate, 
       ToDateTime(max(ts), 'YYYY-MM-dd HH:mm:ss') AS maxDate
from events 
group by $segmentName
order by max(ts) DESC
```

The merge/roll up job runs every 5 minutes, so give it a bit of time and run it again to see the merged segments.