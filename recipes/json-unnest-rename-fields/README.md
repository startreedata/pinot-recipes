# JSON Unnest - Rename Fields

> In this recipe we'll learn how to renamed fields when unnesting/exploding values in nested JSON documents.

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/json-unnest-rename-fields

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/json-unnest-rename-fields
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `movie_ratings` table:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddSchema   \
  -schemaFile /config/schema.json \
  -exec
```

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -exec
```

Import [data/movies.json](data/movies.json) into Pinot:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from movie_ratings 
limit 10
```
