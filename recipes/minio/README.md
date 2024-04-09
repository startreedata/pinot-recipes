# Using MinIO as Deep Store for an Offline Table

> In this recipe we'll learn how to use [MinIO](https://docs.min.io/docs/aws-cli-with-minio) as a Pinot Deep Store.

## Makefile

Clone this repository and navigate to this recipe:

```bash
makre recipe
```

## Validate

Check that minio has the segment in the deep store. You can also log into the minio console and check. http://localhost:9001/browser/deepstore. (username and password is `miniodeepstorage`)

```
docker exec minio mc ls myminio/deepstore/transcript
```

