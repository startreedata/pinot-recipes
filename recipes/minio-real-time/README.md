# Using MinIO as a Deep Store

> In this recipe we'll learn how to use Minio as a Deep Store for segments in real-time tables.


## Makefile

```bash
make recipe
```

## Validate

Check that minio has the segment in the deep store. You can also log into the minio console and check. http://localhost:9001/browser/deepstore. (username and password is `miniodeepstorage`)

```
docker exec minio mc ls myminio/deepstore/events
```

Add table and schema:

```bash
docker run \
   --network minio \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-realtime.json \
     -controllerHost "pinot-controller" \
    -exec
```


Import messages into Kafka:

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t events -Kø
```

List the segments in the MinIO bucket:

```
aws s3 ls s3://pinot-events/events/ \
  --endpoint-url http://localhost:9100 \
  --human-readable 
```
