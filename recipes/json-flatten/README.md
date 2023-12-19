# Flatten JSON documents

> In this recipe we'll learn how to flatten nested fields in JSON documents.

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

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/json-flatten
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Open another tab to add the `users_flatten` table:

```bash
docker run \
   --network json \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema-flatten.json \
     -tableConfigFile /config/table-flatten.json \
     -controllerHost "pinot-controller-json" \
    -exec
```

And now the `users_no_flatten` table:

```bash
docker run \
   --network json \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema-no-flatten.json \
     -tableConfigFile /config/table-no-flatten.json \
     -controllerHost "pinot-controller-json" \
    -exec
```

Import [data/users.json](data/users.json) into Pinot:

```bash
docker run \
   --network json \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml \
  -values tableName='users_no_flatten'
```

```bash
docker run \
   --network json \
   -v $PWD/config:/config \
      -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml \
  -values tableName='users_flatten'
```

Navigate to http://localhost:9000/#/query and run the following queries:

```sql
select * 
from users_no_flatten 
limit 10
```

```sql
select * 
from users_flatten 
limit 10
```
