# Scheduled batch import


```bash
docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```

Update table:

```bash
curl -X PUT "http://localhost:9000/tables/events" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @config/table.json
```

```bash
curl -X GET "http://localhost:9000/tasks/SegmentGenerationAndPushTask/debug?verbosity=0"\
   -H "accept: application/json" 2>/dev/null | jq '.'
```


```bash
 docker exec \
   -e AWS_ACCESS_KEY_ID=xxx \
   -e AWS_SECRET_ACCESS_KEY=yyy \
   -it pinot-controller bin/pinot-admin.sh LaunchDataIngestionJob \
   -jobSpecFile /config/job-spec.yml
```

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`uuidgen | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done | tee "data/events_$(date +'%Y%m%d_%H%M').json"

```