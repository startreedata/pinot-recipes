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
docker-compose up
```

Open another tab to add the `users` table:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddSchema   \
  -schemaFile /config/schema.json \
  -exec
```

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table-no-flatten.json   \
  -exec
```

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table-flatten.json   \
  -exec
```

Import [data/users.json](data/users.json) into Pinot:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml \
  -values tableName='users_no_flatten'
```

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh LaunchDataIngestionJob \
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
