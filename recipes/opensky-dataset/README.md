# OpenSky Dataset

> In this recipe we'll how to import and query the [OpenSky dataset](https://zenodo.org/record/7923702).

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
    <td>Real-Time Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
</table>

<!-- This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-full -->

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/opensky-dataset
```

Download CSV files from https://zenodo.org/record/7923702 and put them into the `data` directory

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add table and schema:

```bash
docker run \
   --network opensky \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-opensky" \
    -exec
```


Ingest the data, making sure that you turn off the multi stage query engine:

```sql
SET taskName = 'flights-dataload';
SET input.fs.className = 'org.apache.pinot.spi.filesystem.LocalPinotFS';
SET includeFileNamePattern='glob:**/*.csv';
INSERT INTO flights 
FROM FILE 'file:///data/';
```

Query the dataset:

```sql
select origin as airport, count(*)
from flights
group by airport
order by count(*) DESC
limit 10
```