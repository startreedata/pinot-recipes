# Filtering reccords during ingestion

> In this recipe we'll learn how to filter records during ingestion.

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
      <tr>
    <td>Ingestion Job</td>
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/filtering-ingestion

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/filtering
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `movies` table:

```bash
docker run \
   --network filtering\
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-filtering" \
    -exec
```

The table config will ensure that ingested record with a `year` value greater than or equal to 2010 will be excluded.

Import [data/ingest.json](data/import.json) into Pinot:

```bash
docker run \
   --network filtering \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
     -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movies 
limit 10
```
