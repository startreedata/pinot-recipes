# Time boundary for hybrid tables

> In this recipe we'll learn how to compute the time boundary used by Pinot brokers when processing queries for hybrid tables

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
    <td>Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/time-boundary-hybrid-table -->

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/time-boundary-hybrid-table
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add table and schema:

```bash
docker run \
   --network rt \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
   -schemaFile /config/schema.json \
   -realtimeTableConfigFile /config/table-realtime.json \
   -offlineTableConfigFile /config/table-offline.json \
   -controllerHost "pinot-controller-rt" \
   -exec
```

Ingest records into the offline table:

```bash
docker run \
   --network rt \
   -v $PWD/config:/config \
   -v $PWD/input:/input \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Import messages into Kafka:

```bash
python datagen.py |
kcat -P -b localhost:9092 -t events
```

Check the time boundary:

```bash
curl "http://localhost:8099/debug/timeBoundary/events" -H "accept: application/json" 2>/dev/null | jq '.'
```

Output:
```json
{
  "timeColumn": "ts",
  "timeValue": "1646993014184"
}
```