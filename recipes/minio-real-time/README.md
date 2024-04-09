# Using MinIO as a Deep Store

> In this recipe we'll learn how to use Minio as a Deep Store for segments in real-time tables.


## Makefile

```bash
make recipe
```

## Validate

Check that minio has the segment in the deep store. You can also log into the minio console and check. http://localhost:9001/browser/deepstore. (username and password is `miniodeepstorage`)

```
docker exec minio mc ls myminio/deepstore/events
```

