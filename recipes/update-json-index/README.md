# Updating a JSON Index

> In this recipe we'll learn how to update a JSON index and have the new config applied to existing data.

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
    <td>Initial Table Config</td>
    <td><a href="config/table.json">config/table.json</a></td>
  </tr>
    <tr>
    <td>Table Config with no index</td>
    <td><a href="config/table-no-index.json">config/table-no-index.json</a></td>
  </tr>
   <tr>
    <td>Updated Table Config</td>
    <td><a href="config/table-updated-index.json">config/table-updated-index.json</a></td>
  </tr>
  
  
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/json-update-index

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/update-json-index
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

Remove the `-arm64` suffix from the Apache Pinot image name if you aren't using the Mac M1/M2.

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

Clear JSON index and refresh all segments:

```bash
docker run \
   --network jsonindex \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-no-index.json \
     -controllerHost "pinot-controller-jsonindex" \
    -exec -update
```

```bash
curl -X 'POST' 'http://localhost:9000/segments/people_REALTIME/reload?type=REALTIME' 
```

Update with new JSON index and refresh all segments:

```bash
docker run \
   --network jsonindex \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
     -schemaFile /config/schema.json \
     -tableConfigFile /config/table-updated-index.json \
     -controllerHost "pinot-controller-jsonindex" \
    -exec -update
```

```bash
curl -X 'POST' 'http://localhost:9000/segments/people_REALTIME/reload?type=REALTIME' 
```

Query Pinot again:

This query will return results:

```sql
select count(*)
from people 
WHERE JSON_MATCH(person, '"$.address.country" = ''Croatia''')
```

But this one won't because that field isn't indexed anymore:

```sql
select count(*)
from people 
WHERE JSON_MATCH(person, '"$.interests[0]" = ''Swimming''')
```
