# Importing CSV files with columns containing spaces

In this recipe we'll learn how to use transformation functions to ingest a CSV file whose column names contain spaces.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.0</td>
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

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add the `crimes` table:

```bash
docker exec -it manual-pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

Import [data/ingest.csv](data/import.csv) into Pinot:

```bash
docker exec -it manual-pinot-controller bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from crimes 
limit 10
```
