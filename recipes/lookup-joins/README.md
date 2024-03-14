# Understanding Lookup-based Join Support in Apache Pinot

> In this recipe we'll learn how to use look up joins in Apache Pinot. 

`lookup` joins in Pinot are done against a dimensional table. Dimension tables are a special kind of offline table. They are replicated on all the hosts for a given tenant to allow faster lookups.

Alternatively, you can perform a join using Pinot's `multi-stage` query engine in cases where the joining table is not dimensional.


This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/lookup-joins


## Steps

Run the make command below. Re-run the command if you encounter any errors.

```bash
make recipe
```

Go to the [Pinot console](http://localhost:9000) and execute the lookup command below.

```sql
SELECT
    orders.order_id,
    lookup('customers','name','customer_id',customer_id) as name,
    lookup('customers','tier','customer_id',customer_id) as tier,
    orders.amount
FROM orders
WHERE tier='Gold'
LIMIT 10
```

