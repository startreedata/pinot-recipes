# Import data files from different directories

> In this recipe we'll learn how to import data files from different directories.

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
cd pinot-recipes/recipes/import-csv-files-different-directories
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `movies` table:

```bash
docker run \
   --network csv \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -tableConfigFile /config/table.json   \
     -schemaFile /config/schema.json \
     -controllerHost "pinot-controller-csv" \
    -exec
```

Import the CSV files from the  [input](input) directory into Pinot:

```bash
docker run \
   --network csv \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   -v $PWD/input:/input \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movies 
limit 10
```
