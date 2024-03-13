# Understanding Lookup-based Join Support in Apache Pinot

> In this recipe we'll learn how to use look up joins in Apache Pinot. 

`lookup` joins in Pinot are done against a dimensional table. Dimension tables are a special kind of offline table. They are replicated on all the hosts for a given tenant to allow faster lookups.

Alternatively, you can perform a join using Pinot's `multi-stage` query engine in cases where the joining table is not dimensional.


This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/lookup-joins


## Steps

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/lookup-joins
```

```bash
docker run \
   --network lookup-join \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
   -schemaFile /config/orders_schema.json \
   -tableConfigFile /config/orders_table.json \
   -controllerHost "pinot-controller" \
   -exec
```

```bash
docker run \
   --network lookup-join \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
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
   apachepinot/pinot:1.0.0 LaunchDataIngestionJob \
-jobSpecFile /config/customers_job-spec.yml
```

```bash
cat data/orders.json |
kcat -P -b localhost:9092 -t orders
```