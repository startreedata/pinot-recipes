# Infer schema from JSON data

> In this recipe we'll learn how to infer a Pinot schema from JSON data

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.3</td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/infer-schema-json-data

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/infer-schema-json-data
```

Spin up a Pinot Controller using Docker Compose:

```bash
docker-compose up
```

Infer schema from  [data/github.json](data/github.json):

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -jsonFile=/data/github.json \
  -outputDir=./config \
  -pinotSchemaName=github \
  -dimensions=""
```

This will write the schema file to [config/github.json](config/github.json).

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -jsonFile=/data/github.json \
  -outputDir=./config \
  -pinotSchemaName=github_with_ts \
  -timeColumnName=created_at
```

This will write the schema file to [config/github_with_ts.json](config/github_with_ts.json).

```bash
docker exec -it pinot-controller-json bin/pinot-admin.sh JsonToPinotSchema \
  -jsonFile=/data/github.json \
  -outputDir=./config \
  -pinotSchemaName=github_with_ts \
  -timeColumnName=created_at \
  -fieldsToUnnest=payload.commits
```

This will write the schema file to [config/github_unnest.json](config/github_unnest.json).
