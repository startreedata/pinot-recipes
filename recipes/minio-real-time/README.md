# Using MinIO as a Deep Store

> In this recipe we'll learn how to use Minio as a Deep Store for segments in real-time tables.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.10.0</td>
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


***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/minio-real-time
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Navigate to http://localhost:9101 and login using the username `minioadmin` and password `minioadmin`. 
Click on `Identity > Users` and create a `miniodeepstorage` user with the password `miniodeepstorage` and assigned the `readwrite` policy.

Configure the [MinIO Demo credentials](https://docs.min.io/docs/aws-cli-with-minio) as environment variables:

```bash
export AWS_ACCESS_KEY_ID="miniodeepstorage" 
export AWS_SECRET_ACCESS_KEY="miniodeepstorage" 
```

Create a S3 bucket called `pinot-events`:

```bash
aws s3 mb s3://pinot-events \
  --endpoint-url http://localhost:9100 
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
