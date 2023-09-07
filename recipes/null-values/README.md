# Handle null values

> In this recipe we'll learn how to work with null values in Apache Pinot.

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
      <tr>
    <td>Ingestion Job</td>
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/handle-null-values


***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/null-values
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Open another tab to add the `movies` schema and table config:

```bash
docker run \
   --network null-values \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-nulls.json \
     -controllerHost "pinot-controller-nulls" \
    -exec
```

Next, add the `movies-no-nulls` table:

```bash
docker run \
   --network null-values \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema-no-nulls.json \
     -tableConfigFile /config/table-no-nulls.json \
     -controllerHost "pinot-controller-nulls" \
    -exec
```

Import [data/ingest.json](data/import.json) into the `movies-not-nulls` and `movies-nulls` tables:

```bash
docker run \
   --network null-values \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
     -jobSpecFile /config/job-spec.yml \
     -values tableName='movies_no_nulls'
```

```bash
docker run \
   --network null-values \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
     -jobSpecFile /config/job-spec.yml \
     -values tableName='movies_nulls'
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movies_no_nulls 
WHERE genre IS NOT NULL
```

```sql
select * 
from movies_nulls 
WHERE genre IS NOT NULL
```