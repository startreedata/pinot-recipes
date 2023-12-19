# Partial Upserts

> In this recipe we'll learn how to use partial upsert functionality.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.0.0</td>
  </tr>
  <tr>
    <td>Schema</td>
    <td><a href="config/schema.json">config/meetup_rsvp_schema.json</a></td>
  </tr>
    <tr>
    <td>Table Config</td>
    <td><a href="config/table.json">config/meetup_rsvp_table.json</a></td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/upserts-partial

***

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/partial-upserts
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add table and schema:

```bash
docker run \
   --network upserts \
   -v $PWD/config:/config \
   apachepinot/pinot:1.0.0 AddTable \
  -tableConfigFile /config/meetup_rsvp_table.json \
  -controllerHost "pinot-controller" \
  -schemaFile /config/meetup_rsvp_schema.json \
  -exec
```

Import messages into Kafka:

```bash
echo - '
{"event_id":3,"venue_name":"Indonesia","group_name":"C","rsvp_count":1,"mtime":"1635140709"}
{"event_id":3,"venue_name":"China","group_name":"C","rsvp_count":1,"mtime":"1646067689"}
{"event_id":2,"venue_name":"France","group_name":"C","rsvp_count":1,"mtime":"1616646138"}
{"event_id":1,"venue_name":"Myanmar","group_name":"B","rsvp_count":1,"mtime":"1632930567"}
{"event_id":1,"venue_name":"Hungary","group_name":"A","rsvp_count":1,"mtime":"1643574332"}
{"event_id":1,"venue_name":"China","group_name":"B","rsvp_count":1,"mtime":"1645779637"}
' | kcat -P -b localhost:9092 -t meetup_rsvp
```

Query Pinot:

```sql
select event_id, sum(rsvp_count) as total_rsvp
from meetup_rsvp 
group by event_id
order by total_rsvp desc
limit 10
```
