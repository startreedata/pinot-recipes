# Working with nested JSON documents

> In this recipe we'll learn how to work with JSON documents using regex, isJson and array functions added in Apache Pinot 1.2.0.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>1.2.0</td>
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
    <td><a href="config/job-spec.yml">config/jobspec.yml</a></td>
  </tr>
</table>

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/json-regex
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Add some data:

```bash
cd data
wget https://data.gharchive.org/2021-07-21-9.json.gz
gunzip *.json.gz
/opt/pinot/bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /config/jobspec.yaml
```

Query Pinot:

```sql
SELECT * FROM github_events WHERE JSON_MATCH(actor_json, 'REGEXP_LIKE("$.[login]", ''Boj*'')')

```

```sql
SELECT * FROM github_events WHERE JSON_MATCH(actor_json, '"$.[id]" > 35560568')
```

```sql
SELECT commit_author_names, isJson(commit_author_names) from github_events limit 10
```