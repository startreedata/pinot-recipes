# StarTree Index

> In this recipe we'll learn how to use the StarTree index.

|Property|Value|
|-|-|
|Pinot Version|1.0.0|


***

## Makefile

Run this recipe using make.

```bash
make recipe
```

This will build up the infrastructure: Pinot and Kafka, create the tables, and produce streaming data. 

Three tables will be generated:

- webtraffic - a real-time table with any Pinot indexes.
- webstraffic_inverted - a real-time table with an `inverted index` on the columns: country, browserType, and deviceBrand.

```json
"invertedIndexColumns": [
  "country",
  "browserType",
  "deviceBrand"
],
```
- webtraffic_startree - a real-time table with a `startree index`.

```json
"starTreeIndexConfigs": [
  {
    "dimensionsSplitOrder": [
      "country",
      "browserType",
      "deviceBrand"
    ],
    "skipStarNodeCreationForDimensions": [],
    "functionColumnPairs": [
      "COUNT__*",
      "SUM__timeSpent",
      "AVG__timeSpent"
    ],
    "maxLeafRecords": 10000
  }
],
```

Open your browser to the [Pinot console](http://localhost:9000) and execute the SQL statements below.


```sql
select browserType, count(*)
from webtraffic 
WHERE country = 'Uruguay'
GROUP BY browserType
limit 10
```

```sql
select country, sum(timeSpent) AS totalTime
from webtraffic
group by country
order by totalTime DESC
limit 10
```

```sql
select count(*), sum(timeSpent) AS totalTime
from webtraffic
where country = 'United Kingdom'
order by totalTime DESC
limit 10
```

```sql
select browserType, count(*)
from webtraffic
WHERE country IN ('Germany', 'United Kingdom', 'Spain')
GROUP BY browserType
limit 10
```

Try changing `FROM webtraffic` to `FROM webtraffic_inverted` or `FROM webtraffic_stree`

