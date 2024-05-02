# Celebrity Look Alike

Have Pinot find the celebrity you resemble the most.

## Download Data

https://www.kaggle.com/datasets/greg115/celebrities-100k?resource=download

https://www.kaggle.com/datasets/jessicali9530/celeba-dataset


https://docs.pinot.apache.org/basics/data-import/from-query-console

```sql
SET taskName = 'myTask-s3';
SET input.fs.className = 'org.apache.pinot.plugin.filesystem.S3PinotFS';
SET input.fs.prop.accessKey = 'my-key';
SET input.fs.prop.secretKey = 'my-secret';
SET input.fs.prop.region = 'us-west-2';
INSERT INTO "baseballStats"
FROM FILE 's3://my-bucket/public_data_set/baseballStats/rawdata/'
```

face1 = face_classifier.detectMultiScale(
    img1, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

face2 = face_classifier.detectMultiScale(
    img2, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)


## Flask

http://127.0.0.1:9100/
