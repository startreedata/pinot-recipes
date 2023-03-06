= Geospatial Indexes

> In this recipe we'll learn how to work with Geospatial indexes

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
    <td>Real-Time Table Config</td>
    <td><a href="config/_table.json">config/table.json</a></td>
  </tr>
</table>

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/geospatial-indexing
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

Add tables and schema:

```bash
docker run \
   --network geospatial \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-geospatial" \
    -exec
```

Sample queries:

```sql
select count(*)
from events_geo 
WHERE ST_Contains(
         toSphericalGeography(ST_GeomFromText('POLYGON((
           -79.68778610229492 39.475226764883985,
           -76.83970928192137 40.48289486417028,
           -75.6193685531616 38.75281151479021,
           -77.61510372161864 37.51568305958246,
           -81.04884624481201 38.86621021801801,
           -79.68778610229492 39.475226764883985))')),
           point
       ) = 1
limit 1
```

```sql
select uuid, ST_AsText(point), ts,
       ST_Distance(point, toSphericalGeography(ST_GeomFromText(
         'POINT(-77.39327430725099 38.93217314143698)'))) AS distance
from events_geo 
WHERE  distance < 50000
limit 10
```

Check that the index is being used:

```sql
EXPLAIN PLAN FOR
select uuid, ST_AsText(point), ts,
       ST_Distance(point, toSphericalGeography(ST_GeomFromText(
         'POINT(-77.39327430725099 38.93217314143698)'))) AS distance
from events_geo 
WHERE  distance < 50000
limit 10
```
