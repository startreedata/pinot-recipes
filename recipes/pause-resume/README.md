# Pause/Resume

> In this recipe we'll learn how to pause and resume consumption from a data stream.

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
cd pinot-recipes/recipes/pause-resume
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network pauseresume \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-pauseresume" \
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
select count(* FROM events
```

Pause consumption:

```bash
curl -X POST \
  "http://localhost:9000/tables/events/pauseConsumption" \
  -H "accept: application/json"
```

Update table config:

```bash
docker run \
   --network pauseresume \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-fixed.json \
     -controllerHost "pinot-controller-pauseresume" \
    -exec -update
```

Resume consumption

```bash
curl -X POST \
  "http://localhost:9000/tables/events/resumeConsumption?consumeFrom=smallest" \
  -H "accept: application/json"
```