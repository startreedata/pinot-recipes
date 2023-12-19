# Configuring segment threshold

> In this recipe we'll learn how to configure the segment threshold for real-time tables

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/configuring-segment-threshold

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/configuring-segment-threshold
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker run \
   --network segment \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-segment" \
    -exec
```

Import message into Kafka:

```bash
python datagen.py | 
kcat -P -b localhost:9092 -t events
```

Query Pinot:

```sql
select * 
from events
```
