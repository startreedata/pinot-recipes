# Understanding Lookup-based Join Support in Apache Pinot

> In this recipe we'll learn how to use look up joins in Apache Pinot. 

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/lookup-joins

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/lookup-joins
```

```bash
docker run \
   --network lookup-join \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
   -schemaFile /config/orders_schema.json \
   -tableConfigFile /config/orders_table.json \
   -controllerHost "pinot-controller" \
   -exec
```

```bash
docker run \
   --network lookup-join \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
   -schemaFile /config/customers_schema.json \
   -tableConfigFile /config/customers_table.json \
   -controllerHost "pinot-controller" \
   -exec
```

```bash
docker run \
   --network lookup-join \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob \
-jobSpecFile /config/customers_job-spec.yml
```

```bash
cat data/orders.json |
kcat -P -b localhost:9092 -t orders
```