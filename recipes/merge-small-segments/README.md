# Merge small segments

> In this recipe we'll learn how to merge small segments in offline tables.

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
      <tr>
    <td>Ingestion Job</td>
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/merge-small-segments

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/merge-small-segments
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `movies` table:

```bash
docker run \
   --network mergesegments \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-mergesegments" \
    -exec
```

Import the CSV files from the [input](input) directory into Pinot:

```bash
docker run \
   --network mergesegments \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   -v $PWD/input:/input \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
    -jobSpecFile /config/job-spec.yml \
    -values pinotController=http://pinot-controller-mergesegments:9000
```

Run the following to get a list of segments:

```bash
segments_breakdown () {
  table="matches"
  table_type="OFFLINE"
  segments=$(curl -X GET "http://localhost:9000/segments/${table}?type=${table_type}"  2>/dev/null | jq -r '.[] []')

  for segment in $(echo $segments | jq '.[]'); do 
    metadata=`curl -X GET "http://localhost:9000/segments/${table}/$(echo ${segment} | jq -r)/metadata" \
      -H "accept: application/json" 2>/dev/null | jq '.'`
    docs=`echo $metadata | jq '."segment.total.docs" | tonumber'`
    startTime=`echo $metadata | jq '."segment.start.time" | tonumber'`
    endTime=`echo $metadata | jq '."segment.end.time" | tonumber'`
    echo "$segment,$docs,$startTime,$endTime"
  done
}

segments_breakdown
```

Run the Merge Roll Up Job:

```bash
curl -X POST "http://localhost:9000/tasks/schedule?taskType=MergeRollupTask&tableName=matches_OFFLINE" \
  -H "accept: application/json" 2>/dev/null | jq '.'
```

List the segments again:

```bash
segments_breakdown
```
