# Using Google Cloud Storage as a Deep Store

> In this recipe we'll learn how to use Google Cloud Storage as a Deep Store for segments in real-time tables.

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
cd pinot-recipes/recipes/google-cloud-storage
```

Navigate to https://console.cloud.google.com/storage/browser and create a bucket e.g. `pinot-events`
Update the following lines in config/controller-conf.conf[config/controller-conf.conf]:

[source, text]
----
controller.data.dir=gs://<bucket-name>
pinot.controller.storage.factory.gs.projectId=<project-id>
----

* Replace `<bucket-name>` with the name of your bucket.
* Replace `<project-id>` with the name of your GCP project.

Paste the contents of your GCP JSON key file into config/service-account.json[config/service-account.json]

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-gcs bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table-realtime.json   \
  -schemaFile /config/schema.json -exec
```

Import messages into Kafka:

```bash
while true; do
  ts=`date +%s%N | cut -b1-13`;
  uuid=`cat /proc/sys/kernel/random/uuid | sed 's/[-]//g'`
  count=$[ $RANDOM % 1000 + 0 ]
  echo "{\"ts\": \"${ts}\", \"uuid\": \"${uuid}\", \"count\": $count}"
done |
docker exec -i kafka-gcs /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic events
```

List the segments in the Google Cloud Storage bucket:

```
bucketName="pinot-events"
gsutil ls -l gs://${bucketName}/events/
```
