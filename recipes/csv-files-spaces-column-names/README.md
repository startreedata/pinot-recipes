# Importing CSV files with columns containing spaces

Pinot can transform data at ingestion. In this recipe, we'll learn how to use a transformation to change the name of a column. We will ingest a CSV file with a column containing spaces in its name. 

```csv
ID,Case Number
10224738,HY411648
10224739,HY411615
11646166,JC213529
10224740,HY411595
```

We will use a transformation function to remove the space as the data is being ingested into Pinot

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/csv-files-spaces-column-names

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/csv-files-spaces-column-names
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `crimes` table:

```bash
docker run \
   --network csv \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-csv" \
    -exec
```

Import [data/ingest.csv](data/import.csv) into Pinot:

```bash
docker run \
   --network csv \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from crimes 
limit 10
```
