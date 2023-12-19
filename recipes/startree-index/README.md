# StarTree Index

> In this recipe we'll learn how to use the StarTree index.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
  </tr>
</table>

***

## Setup

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/startree-index
```

Start up Pinot and friends:

```bash
docker compose up
```

## Create topic

```bash
rpk topic create -p 5 webtraffic
```

## Run data generator

```bash
poetry run python datagen.py 2>/dev/null | 
jq -cr --arg sep ø '[.userID, tostring] | join($sep)' | 
kcat -P -b localhost:9092 -t webtraffic -Kø
```

## Create Tables

```bash
docker run \
   --network startree-index \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/base/schema.json \
     -tableConfigFile /config/base/table.json \
     -controllerHost "pinot-controller-startree-index" \
    -exec
```

```bash
docker run \
   --network startree-index \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/startree/schema.json \
     -tableConfigFile /config/startree/table.json \
     -controllerHost "pinot-controller-startree-index" \
    -exec
```

```bash
docker run \
   --network startree-index \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/inverted/schema.json \
     -tableConfigFile /config/inverted/table.json \
     -controllerHost "pinot-controller-startree-index" \
    -exec
```

## Queries

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

