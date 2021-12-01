# Importing CSV files with columns containing spaces


```bash
docker-compose up
```

```bash
docker exec -it manual-pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

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