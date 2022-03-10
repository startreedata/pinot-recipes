# Chaining Transformation Functions

> In this recipe we'll learn how to chain transformation functions.

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
      <tr>
    <td>Ingestion Job</td>
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/chaining-transformation-functions

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/chaining-transformation-functions
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `people` table:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

Import [data/ingest.json](data/import.json) into Pinot:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from people 
limit 10
```
