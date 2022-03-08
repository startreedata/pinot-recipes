# Infer schema from JSON data

> In this recipe we'll learn how to infer a Pinot schema from JSON data

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.3</td>
  </tr>
</table>

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/infer-schema-json-data
```

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

Import [data/ingest.json](data/import.json) into Pinot:

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -jsonFile=/data/github.json \
  -outputDir=./config \
  -pinotSchemaName=github \
  -dimensions=""
```

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -jsonFile=/data/github.json \
  -outputDir=./config \
  -pinotSchemaName=github_with_ts \
  -timeColumnName=created_at
```