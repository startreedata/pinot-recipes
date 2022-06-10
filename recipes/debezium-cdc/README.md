# Apache Pinot and Debezium Example for MySQL

Spin up a Pinot cluster using Docker Compose:

```bash
docker-compose up
```

```bash
docker exec -it pinot-controller-cdc bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json   \
  -schemaFile /config/schema.json \
  -exec
```

```bash
curl -i -X POST \
  -H "Accept:application/json" \
  -H  "Content-Type:application/json" \
  http://localhost:8083/connectors/ \
  -d @debezium/register-mysql.json
```

```bash
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory -e "UPDATE customers SET first_name=\"Anne Sue\" WHERE id=1004;"'
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory -e "UPDATE customers SET first_name=\"Kyle\" WHERE id=1003;"'
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory -e "UPDATE customers SET last_name=\"Johannson\" WHERE id=1002;"'
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory -e "UPDATE customers SET first_name=\"Jane\", last_name=\"Appleseed\" WHERE id=1001;"'
```