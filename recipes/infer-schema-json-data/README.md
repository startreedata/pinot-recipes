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

Infer schema from  [data/github.json](data/github.json):

```bash
docker run \
  -v ${PWD}/data/github.json:/data/github.json \
  -v ${PWD}/config:/config \
  apachepinot/pinot:0.9.3 JsonToPinotSchema \
  -jsonFile /data/github.json \
  -pinotSchemaName="github" \
  -outputDir="/config" \
  -dimensions=""
```

This will write the schema file to [config/github.json](config/github.json).

```bash
docker run \
  -v ${PWD}/data/github.json:/data/github.json \
  -v ${PWD}/config:/config \
  apachepinot/pinot:0.9.3 JsonToPinotSchema \
  -jsonFile /data/github.json \
  -pinotSchemaName="github_with_ts" \
  -outputDir="/config" \
  -timeColumnName=created_at
```

This will write the schema file to [config/github_with_ts.json](config/github_with_ts.json).

```bash
docker run \
  -v ${PWD}/data/github.json:/data/github.json \
  -v ${PWD}/config:/config \
  apachepinot/pinot:0.9.3 JsonToPinotSchema \
  -jsonFile /data/github.json \
  -pinotSchemaName="github_unnest" \
  -outputDir="/config" \
  -timeColumnName=created_at \
  -fieldsToUnnest=payload.commits
```

This will write the schema file to [config/github_unnest.json](config/github_unnest.json).
