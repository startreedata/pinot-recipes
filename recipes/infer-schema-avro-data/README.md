# Infer schema from JSON data

> In this recipe we'll learn how to infer a Pinot schema from JSON data

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.12.0</td>
  </tr>
</table>

This is the code for the following recipe: https://dev.startree.ai/docs/pinot/recipes/infer-schema-json-data

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/infer-schema-avro-data
```

Infer schema from  [data/github.json](data/github.json):

```bash
docker run \
  -v ${PWD}/config:/config \
  -v ${PWD}/avro:/avro \
  apachepinot/pinot:0.12.0-arm64 AvroSchemaToPinotSchema \
  -avroSchemaFile /avro/mastodon-topic-value.avsc \
  -pinotSchemaName="mastodon" \
  -outputDir="/config" \
  -dimensions="" \
  -timeColumnName "created_at" \
  -metrics "favourites,words,characters,tags"
```

This will write the schema file to [config/mastodon.json](config/mastodon.json).
