# Pulsar

> In this recipe we'll learn how to ingest data from Apache Pulsar.

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
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/pulsar

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/pulsar
```

Download the appropriate version of the Pulsar plugin from https://central.sonatype.com/artifact/org.apache.pinot/pinot-pulsar/versions and copy it into the `plugins` directory

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add table and schema:

```bash
docker run \
   --network pulsar \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
   -schemaFile /config/schema.json \
   -tableConfigFile /config/table.json \
   -controllerHost "pinot-controller-pulsar" \
   -exec
```

Import message into Pulsar:

```bash
python -m venv .venv
source .venv/bin/active
pip install pulsar-client
```

```bash
python producer.py
```

Query Pinot:

```sql
select * 
from events
```
