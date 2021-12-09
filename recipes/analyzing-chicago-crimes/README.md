# Analyzing Chicago Crimes


> In this recipe we'll learn how to use transformation functions to ingest a CSV file whose column names contain spaces.

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

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/analyzing-chicago-crimes
```

Download the Chicago Crimes dataset:

```bash
curl "https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*" -o data/Crimes_-_2001_to_Present.csv
```

Setup Python environment:

```bash
pipenv shell
pipenv install
```

Clean up the data so that it's sorted by the `Beat` column:

```bash
python data_cleanup.py
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Open another tab to add the `crimes` table:

```bash
docker exec -it manual-pinot-controller-chicago bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

Import [data/ingest.csv](data/import.csv) into Pinot:

```bash
docker exec -it manual-pinot-controller-chicago bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile /config/job-spec.yml
```

Run Streamlit app:

```bash
streamlit run app.py
```

Navigate to http://localhost:8501/
