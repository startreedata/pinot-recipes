# Geospatial Default Values

> In this recipe we'll learn how to add a default value for a Geospatial column.

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
    <td>Real-Time Table Config</td>
    <td><a href="config/_table.json">config/table.json</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/geospatial

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/geospatial-default
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Ingest data into Kafka:

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

Add schema:

```bash
docker run \
   --network geospatial \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddSchema \
     -schemaFile /config/schema.json \
     -controllerHost "pinot-controller-geospatial" \
    -exec
```

Add table:

```bash
curl -X POST http://localhost:9000/tables --data @config/table.json


```

Sample queries:

```sql
select StDistance(ST_GeomFromText('POINT (0.6861134172138761 83.5002942140996)'), toGeometry(point)) AS distance, 
       count(*)
from events 
group by distance
order by count(*) DESC, distance desc
limit 10
```