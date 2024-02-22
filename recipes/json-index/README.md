# JSON Indexes

> In this recipe we'll learn how to configure a JSON index.

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

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/json-index

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/json-index
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add tables and schema:

```bash
docker run \
   --network jsonindex \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table.json \
     -controllerHost "pinot-controller-jsonindex" \
    -exec
```

Import messages into Kafka:

```bash
pip install faker
```

```bash
python datagen.py --sleep 0.0001 2>/dev/null |
jq -cr --arg sep ø '[.uuid, tostring] | join($sep)' |
kcat -P -b localhost:9092 -t people -Kø
```

Query Pinot:

```sql
select *
from people 
WHERE JSON_MATCH(person, '"$.address.state"=''Kentucky''')
limit 10
```

```sql
select count(*)
from people 
WHERE JSON_MATCH(person, '"$.address.state" <> ''Kentucky''')
```

```sql
select json_extract_scalar(person, '$.address.state', 'STRING') AS state, count(*)
from people 
WHERE JSON_MATCH(person, '"$.address.state" IN (''Kentucky'', ''Alabama'')')
GROUP BY state
ORDER BY count(*) DESC
```

```sql
select json_extract_scalar(person, '$.address.state', 'STRING') AS state, count(*)
from people 
WHERE JSON_MATCH(person, '"$.address.state" NOT IN (''Kentucky'', ''Alabama'')')
GROUP BY state
ORDER BY count(*) DESC
```

```sql
select count(*)
from people 
WHERE JSON_MATCH(person, '"$.address.state" IN (''Kentucky'')')
```



```sql
select count(*)
from people 
WHERE JSON_MATCH(person, '"$.interests[0]" = ''Swimming''')
```
