# Scheduled batch import


```bash
docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
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
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done > "data/events_$(date +'%Y%m%d_%H%M').json"

```