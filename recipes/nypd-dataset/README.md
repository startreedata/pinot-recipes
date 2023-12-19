# NYPD Dataset

> In this recipe we'll how to import and query the [NYPD dataset](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243).

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
cd pinot-recipes/recipes/nypd-dataset
```

Download CSV files from https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243 and put them into the `data` directory

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add table and schema:

```bash
docker run \
   --network nypd \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-nypd" \
    -exec
```


Ingest the data, making sure that you turn off the multi stage query engine:

```sql
SET taskName = 'nypd-dataload';
SET input.fs.className = 'org.apache.pinot.spi.filesystem.LocalPinotFS';
SET includeFileNamePattern='glob:**/*.csv';
INSERT INTO nypdComplaintData 
FROM FILE 'file:///data/';
```

Query the dataset:

```sql
select boroNm, count(*)
from nypdComplaintData 
group by boroNm
order by count(*) DESC
limit 10
```