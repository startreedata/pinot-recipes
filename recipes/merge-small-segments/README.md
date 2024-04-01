# Merge small segments

> In this recipe we'll learn how to merge small segments in offline tables.


This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/merge-small-segments


## Makefile

```bash
make recipe
```


```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø

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
