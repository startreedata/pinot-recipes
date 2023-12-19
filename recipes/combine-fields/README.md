# Combine fields during import

> In this recipe we'll learn how to combine the data from fields in our data source into a single column in Apache Pinot.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
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
cd pinot-recipes/recipes/combine-fields
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `people` table:

```bash
docker run \
   --network combine \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-combine" \
    -exec
```

Import [data/ingest.json](data/import.json) into Pinot:

```bash
docker run \
   --network combine \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml

docker exec -it pinot-controller-combine bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from people 
limit 10
```
