# Using MinIO as Deep Store for an Offline Table

> In this recipe we'll learn how to use [MinIO](https://docs.min.io/docs/aws-cli-with-minio) as a Pinot Deep Store.

<table>
  <tr>
    <td>Pinot Version</td>
    <td>0.9.0</td>
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
    <td><a href="config/job-spec.yml">config/job-spec.yml</a></td>
  </tr>
        <tr>
    <td>Pre Requisites</td>
    <td>Install the <a href="https://aws.amazon.com/cli/">AWS Command Line Interface</a></td>
  </tr>
</table>

***

Clone this repository and navigate to this recipe:

```bash
git clone git@github.com:startreedata/pinot-recipes.git
cd pinot-recipes/recipes/minio
```

Configure the [MinIO Demo credentials](https://docs.min.io/docs/aws-cli-with-minio) as environment variables:

```bash
export AWS_ACCESS_KEY_ID="Q3AM3UQ867SPQQA43P2F" 
export AWS_SECRET_ACCESS_KEY="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG" 
```

Create an S3 bucket called `pinot-transcript-output`:

```bash
aws --endpoint-url https://play.min.io:9000 s3 mb s3://pinot-transcript-output --region us-east-1

```

Spin up a Pinot cluster using Docker Compose:

```bash
docker compose up
```

Open another tab to add the `transcript` table:

```bash
docker run \
   --network minio \
   -v $PWD/config:/config \
   apachepinot/pinot:0.12.0-arm64 AddTable \
   -schemaFile /config/schema.json \
   -tableConfigFile /config/table.json \
   -controllerHost "manual-pinot-controller-minio" \
   -exec
```

Import [data/transcript.csv](data/transcript.csv) into Pinot:

```bash
docker run \
   --network minio \
   -v $PWD/config:/config \
   -v $PWD/data:/data \
   apachepinot/pinot:0.12.0-arm64 LaunchDataIngestionJob   \
  -jobSpecFile /config/job-spec.yml \
  -values ACCESS_KEY=${AWS_ACCESS_KEY_ID} SECRET_KEY=${AWS_SECRET_ACCESS_KEY}
```

Navigate to http://localhost:9000/#/query and run the following query:

```sql
select * 
from transcript 
limit 10
```

Finally, run the following command to see a `tar.gz` file containing transcript segment data:

```bash
aws --endpoint-url https://play.min.io:9000 s3 ls s3://pinot-transcript-output
```

You should see something like the following:

```
2021-12-01 16:51:57       1718 transcript_OFFLINE_0.tar.gz
```
