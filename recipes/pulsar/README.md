# Pulsar

> In this recipe we'll learn how to ingest data from Apache Pulsar.

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



***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/pulsar
```

Build Pulsar plugin:

```bash
git clone git@github.com:apache/pinot.git
cd pinot
git checkout release-0.10.0
```

```bash
cd pinot-plugins/pinot-stream-ingestion/pinot-pulsar
mvn clean install -DskipTests
```

The Pulsar plugin is in `target/pinot-pulsar-0.10.0-shaded.jar` and we'll copy that into the `plugins` directory.

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker exec -it pinot-controller-pulsar bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json -exec
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
