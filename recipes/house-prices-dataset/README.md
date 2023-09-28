# UK House Prices Dataset

> In this recipe we'll how to import and query the [UK House Prices dataset](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#yearly-file).

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
cd pinot-recipes/recipes/house-prices-dataset
```

Download CSV files from https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#yearly-file and put them into the `raw` directory.
Then use the `clean_csv.py` script to add a header to the file and write it to the `data` directory.

```bash
python clean_csv pp-2021.csv
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Add table and schema:

```bash
docker run \
   --network houseprices \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-houseprices" \
    -exec
```


Ingest the data, making sure that you turn off the multi stage query engine:

```sql
SET taskName = 'houseprices-dataload';
SET input.fs.className = 'org.apache.pinot.spi.filesystem.LocalPinotFS';
SET includeFileNamePattern='glob:**/pp-clean*.csv';
INSERT INTO house_prices 
FROM FILE 'file:///data/';
```

Query the dataset:

```sql
select County, avg(Price) AS averagePrice, count(*) AS numberOfSales
from house_prices
group by County
order by averagePrice DESC
limit 10
```


```sql
select TownCity, County, max(Price) AS maxPrice,
       count(*) AS numberOfSales
from house_prices
WHERE year(TransferDate) = 2021
group by TownCity, County
order by maxPrice DESC
limit 10
```

