# Ingest JSON files from S3


```bash
docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
```


```bash
 docker exec \
   -e AWS_ACCESS_KEY_ID=<access-key-id> \
   -e AWS_SECRET_ACCESS_KEY=<secret-access-key> \
   -it pinot-controller bin/pinot-admin.sh LaunchDataIngestionJob \
   -jobSpecFile /config/job-spec.yml
```


```bash
export AWS_ACCESS_KEY_ID="<access-key-id>"
export AWS_SECRET_ACCESS_KEY="<secret-access-key>"
```

```bash
aws s3 ls s3://marks-st-cloud-bucket/events/
aws s3 cp s3://marks-st-cloud-bucket/events/events_20220615_1533.json .
```

## Generate events

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done > "data/events_$(date +'%Y%m%d_%H%M').json"
```